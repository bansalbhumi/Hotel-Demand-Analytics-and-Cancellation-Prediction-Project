"""
src/monitoring.py — Model Drift Detection & Monitoring
Hotel Intelligence Platform (HIP) — Phase 7

Responsibilities:
  - Compute feature distribution statistics (reference vs. current)
  - Detect data drift using Population Stability Index (PSI)
  - Detect prediction drift (shift in output distribution)
  - Log prediction events to a SQLite audit log
  - Generate a human-readable drift report (JSON + console summary)

Usage (standalone):
    python src/monitoring.py

Usage (from code):
    from src.monitoring import DriftMonitor
    monitor = DriftMonitor()
    monitor.log_prediction(features_dict, probability)
    report  = monitor.run_drift_report()
"""

import os
import json
import logging
import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA = BASE_DIR / "data" / "processed" / "hotel_bookings_cleaned.csv"
AUDIT_DB = BASE_DIR / "data" / "processed" / "prediction_audit.db"
DRIFT_REPORT = BASE_DIR / "reports" / "drift_report.json"

# ─────────────────────────────────────────────────────────────────────────────
# PSI helpers
# ─────────────────────────────────────────────────────────────────────────────
PSI_THRESHOLDS = {
    "stable":   0.10,   # PSI < 0.10  → no significant drift
    "moderate": 0.20,   # 0.10–0.20  → moderate drift — investigate
    # PSI > 0.20  → significant drift — retrain
}

NUMERIC_FEATURES = ["lead_time", "total_of_special_requests", "previous_cancellations",
                    "total_nights", "total_guests"]
CATEGORICAL_FEATURES = ["deposit_type", "market_segment", "customer_type", "season"]


def _psi_label(psi: float) -> str:
    if psi < PSI_THRESHOLDS["stable"]:
        return "stable"
    if psi < PSI_THRESHOLDS["moderate"]:
        return "moderate_drift"
    return "significant_drift"


def compute_psi_numeric(reference: pd.Series, current: pd.Series, bins: int = 10) -> float:
    """
    Compute PSI for a numeric feature.
    PSI = Σ (actual% − expected%) × ln(actual% / expected%)
    """
    # Build bins on the reference distribution
    breakpoints = np.linspace(reference.min(), reference.max(), bins + 1)
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    ref_counts = np.histogram(reference, bins=breakpoints)[0]
    cur_counts = np.histogram(current, bins=breakpoints)[0]

    # Avoid divide-by-zero
    ref_pct = np.where(ref_counts == 0, 1e-4, ref_counts / len(reference))
    cur_pct = np.where(cur_counts == 0, 1e-4, cur_counts / len(current))

    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return float(psi)


def compute_psi_categorical(reference: pd.Series, current: pd.Series) -> float:
    """Compute PSI for a categorical feature."""
    all_cats = set(reference.unique()) | set(current.unique())
    ref_pct = reference.value_counts(normalize=True).reindex(all_cats, fill_value=1e-4)
    cur_pct = current.value_counts(normalize=True).reindex(all_cats, fill_value=1e-4)
    psi = float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))
    return psi


# ─────────────────────────────────────────────────────────────────────────────
# Audit Log (SQLite)
# ─────────────────────────────────────────────────────────────────────────────

class AuditLogger:
    """Persists every prediction call to a local SQLite database."""

    def __init__(self, db_path: Path = AUDIT_DB) -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp       TEXT    NOT NULL,
                    request_hash    TEXT    NOT NULL,
                    features_json   TEXT    NOT NULL,
                    probability     REAL    NOT NULL,
                    risk_label      TEXT    NOT NULL,
                    prediction      INTEGER NOT NULL
                )
            """)
            conn.commit()

    def log(
        self,
        features: dict[str, Any],
        probability: float,
        risk_label: str,
        prediction: int,
    ) -> None:
        features_json = json.dumps(features, sort_keys=True, default=str)
        request_hash = hashlib.md5(features_json.encode()).hexdigest()
        ts = datetime.now(timezone.utc).isoformat()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT INTO predictions
                   (timestamp, request_hash, features_json, probability, risk_label, prediction)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (ts, request_hash, features_json, probability, risk_label, prediction),
            )
            conn.commit()

    def load_recent(self, n: int = 500) -> pd.DataFrame:
        """Load the most recent n predictions."""
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(
                f"SELECT * FROM predictions ORDER BY id DESC LIMIT {n}", conn
            )
        if df.empty:
            return df
        # Expand features_json back into columns
        features_df = pd.json_normalize(df["features_json"].apply(json.loads))
        return pd.concat([df[["timestamp", "probability", "risk_label", "prediction"]],
                          features_df], axis=1)

    def total_predictions(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]


# ─────────────────────────────────────────────────────────────────────────────
# Drift Monitor
# ─────────────────────────────────────────────────────────────────────────────

class DriftMonitor:
    """
    Compares live prediction inputs against the training distribution (reference)
    to surface feature drift and prediction drift.

    Typical workflow:
        monitor = DriftMonitor()
        monitor.log_prediction(features, prob, risk_label, prediction)
        report  = monitor.run_drift_report(min_samples=100)
    """

    def __init__(
        self,
        reference_data_path: Path = PROCESSED_DATA,
        db_path: Path = AUDIT_DB,
    ) -> None:
        self.audit = AuditLogger(db_path)
        logger.info("Loading reference distribution from %s", reference_data_path)
        self.reference = pd.read_csv(reference_data_path)

    # ── Public interface ─────────────────────────────────────────────────────

    def log_prediction(
        self,
        features: dict[str, Any],
        probability: float,
        risk_label: str = "",
        prediction: int = -1,
    ) -> None:
        """Record a single prediction event to the audit log."""
        if not risk_label:
            pct = probability * 100
            risk_label = "High" if pct > 60 else ("Moderate" if pct > 30 else "Low")
        if prediction == -1:
            prediction = 1 if probability >= 0.5 else 0
        self.audit.log(features, probability, risk_label, prediction)

    def run_drift_report(self, min_samples: int = 50) -> dict:
        """
        Compute feature + prediction drift between the reference dataset
        and the most-recent live predictions stored in the audit log.

        Returns a dict report and also writes it to reports/drift_report.json.
        """
        total = self.audit.total_predictions()
        if total < min_samples:
            logger.warning(
                "Only %d predictions logged — need at least %d for a reliable drift report.",
                total, min_samples,
            )

        current = self.audit.load_recent(n=500)
        if current.empty:
            return {"error": "No predictions logged yet."}

        report: dict = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_predictions_logged": total,
            "samples_analysed": len(current),
            "feature_drift": {},
            "prediction_drift": {},
            "overall_status": "stable",
        }

        # ── Feature drift ────────────────────────────────────────────────────
        any_significant = False

        for feat in NUMERIC_FEATURES:
            if feat not in self.reference.columns or feat not in current.columns:
                continue
            ref_s = self.reference[feat].dropna()
            cur_s = current[feat].dropna()
            if cur_s.empty:
                continue
            psi = compute_psi_numeric(ref_s, cur_s)
            label = _psi_label(psi)
            report["feature_drift"][feat] = {"psi": round(psi, 4), "status": label}
            if label == "significant_drift":
                any_significant = True

        for feat in CATEGORICAL_FEATURES:
            if feat not in self.reference.columns or feat not in current.columns:
                continue
            ref_s = self.reference[feat].dropna()
            cur_s = current[feat].dropna()
            if cur_s.empty:
                continue
            psi = compute_psi_categorical(ref_s, cur_s)
            label = _psi_label(psi)
            report["feature_drift"][feat] = {"psi": round(psi, 4), "status": label}
            if label == "significant_drift":
                any_significant = True

        # ── Prediction drift ─────────────────────────────────────────────────
        ref_cancel_rate = float(self.reference["is_canceled"].mean())
        live_cancel_rate = float(current["prediction"].mean())
        live_avg_prob = float(current["probability"].mean())
        risk_dist = current["risk_label"].value_counts(normalize=True).round(3).to_dict()

        pred_drift_pct = abs(live_cancel_rate - ref_cancel_rate) / max(ref_cancel_rate, 1e-4)
        pred_drift_status = "stable" if pred_drift_pct < 0.15 else (
            "moderate_drift" if pred_drift_pct < 0.30 else "significant_drift"
        )

        report["prediction_drift"] = {
            "reference_cancellation_rate": round(ref_cancel_rate, 4),
            "live_cancellation_rate": round(live_cancel_rate, 4),
            "relative_change_pct": round(pred_drift_pct * 100, 2),
            "avg_probability": round(live_avg_prob, 4),
            "risk_distribution": risk_dist,
            "status": pred_drift_status,
        }

        if pred_drift_status == "significant_drift":
            any_significant = True

        report["overall_status"] = "significant_drift" if any_significant else (
            "moderate_drift"
            if any(v["status"] == "moderate_drift" for v in report["feature_drift"].values())
            else "stable"
        )

        # ── Persist report ───────────────────────────────────────────────────
        DRIFT_REPORT.parent.mkdir(parents=True, exist_ok=True)
        with open(DRIFT_REPORT, "w") as f:
            json.dump(report, f, indent=2)

        self._log_summary(report)
        return report

    # ── Internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _log_summary(report: dict) -> None:
        status = report["overall_status"]
        emoji = {"stable": "✅", "moderate_drift": "⚠️", "significant_drift": "🚨"}.get(status, "❓")
        logger.info("%s Overall drift status: %s", emoji, status.upper())
        logger.info("   Predictions analysed : %d", report["samples_analysed"])
        logger.info("   Prediction drift      : %s", report["prediction_drift"]["status"])
        for feat, info in report["feature_drift"].items():
            if info["status"] != "stable":
                logger.warning("   Feature '%s' — PSI=%.4f (%s)", feat, info["psi"], info["status"])
        logger.info("   Full report → %s", DRIFT_REPORT)


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry-point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys as _sys
    _sys.path.insert(0, str(BASE_DIR))  # ensure project root is importable

    monitor = DriftMonitor()

    # Simulate 200 prediction events drawn from the training data so the
    # report has something to work with on a fresh install.
    from src.inference import CancellationPredictor

    predictor = CancellationPredictor()
    df = pd.read_csv(PROCESSED_DATA)
    sample = df.sample(n=min(200, len(df)), random_state=42)

    logger.info("Simulating %d prediction events…", len(sample))
    for _, row in sample.iterrows():
        features = {
            "deposit_type": row.get("deposit_type", "No Deposit"),
            "country": row.get("country", "PRT"),
            "market_segment": row.get("market_segment", "Online TA"),
            "customer_type": row.get("customer_type", "Transient"),
            "lead_time_bucket": row.get("lead_time_bucket", "31-90"),
            "season": row.get("season", "Summer"),
            "lead_time": int(row.get("lead_time", 50)),
            "total_of_special_requests": int(row.get("total_of_special_requests", 0)),
            "previous_cancellations": int(row.get("previous_cancellations", 0)),
            "total_nights": int(row.get("total_nights", 3)),
            "total_guests": int(row.get("total_guests", 2)),
            "prior_cancel_flag": int(row.get("prior_cancel_flag", 0)),
        }
        prob = float(predictor.predict_proba(pd.DataFrame([features]))[0])
        monitor.log_prediction(features, prob)

    report = monitor.run_drift_report(min_samples=10)
    print(json.dumps(report, indent=2))
