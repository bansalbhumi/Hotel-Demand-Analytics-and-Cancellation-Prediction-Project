"""
FastAPI Application — Hotel Intelligence Platform (HIP)
Serves the Cancellation Prediction model via a REST API.
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from typing import Any, Literal

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# Ensure src/ is importable
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.inference import CancellationPredictor
from src.monitoring import DriftMonitor

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singletons
# ---------------------------------------------------------------------------
predictor: CancellationPredictor | None = None
monitor: DriftMonitor | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the model and drift monitor on startup; release on shutdown."""
    global predictor, monitor
    try:
        predictor = CancellationPredictor()
        logger.info("Model loaded successfully.")
    except FileNotFoundError as exc:
        logger.error(str(exc))
        predictor = None
    try:
        monitor = DriftMonitor()
        logger.info("Drift monitor initialised.")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Drift monitor could not initialise: %s", exc)
        monitor = None
    yield
    predictor = None
    monitor = None
    logger.info("Shutdown complete.")


# ---------------------------------------------------------------------------
# App Initialisation
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Hotel Intelligence Platform API",
    description=(
        "REST API for the Hotel Demand Analytics and Cancellation Prediction project. "
        "Accepts booking features and returns a cancellation probability score."
    ),
    version="1.0.0",
    contact={"name": "Bhumi Bansal"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class BookingFeatures(BaseModel):
    """Input features required for cancellation prediction."""

    hotel: Literal["City Hotel", "Resort Hotel"] = Field(..., description="Hotel Type")
    arrival_date_month: Literal["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    stays_in_weekend_nights: int = Field(..., ge=0)
    stays_in_week_nights: int = Field(..., ge=0)
    adults: int = Field(..., ge=0)
    children: int = Field(..., ge=0)
    babies: int = Field(..., ge=0)
    meal: str = Field(default="BB")
    country: str = Field(..., description="ISO 3166-1 alpha-3 country code of the guest (e.g. PRT).")
    market_segment: Literal[
        "Online TA", "Offline TA/TO", "Groups", "Direct", "Corporate", "Aviation", "Complementary"
    ] = Field(..., description="Booking market segment.")
    distribution_channel: str = Field(default="TA/TO")
    is_repeated_guest: int = Field(default=0)
    previous_cancellations: int = Field(..., ge=0, description="Number of previous cancellations by this guest.")
    previous_bookings_not_canceled: int = Field(default=0)
    reserved_room_type: str = Field(default="A")
    deposit_type: Literal["No Deposit", "Non Refund", "Refundable"] = Field(
        ..., description="Deposit type for the booking."
    )
    customer_type: Literal["Transient", "Transient-Party", "Contract", "Group"] = Field(
        ..., description="Type of customer."
    )
    adr: float = Field(..., ge=0)
    required_car_parking_spaces: int = Field(default=0)
    total_of_special_requests: int = Field(..., ge=0, le=5, description="Number of special requests made.")
    lead_time: int = Field(..., ge=0, le=700, description="Days between booking date and arrival date.")

    @field_validator("country")
    @classmethod
    def uppercase_country(cls, v: str) -> str:
        return v.strip().upper()

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a DataFrame compatible with the training feature set."""
        return pd.DataFrame([self.model_dump()])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "hotel": "City Hotel",
                    "arrival_date_month": "August",
                    "stays_in_weekend_nights": 1,
                    "stays_in_week_nights": 2,
                    "adults": 2,
                    "children": 0,
                    "babies": 0,
                    "meal": "BB",
                    "country": "PRT",
                    "market_segment": "Online TA",
                    "distribution_channel": "TA/TO",
                    "is_repeated_guest": 0,
                    "previous_cancellations": 0,
                    "previous_bookings_not_canceled": 0,
                    "reserved_room_type": "A",
                    "deposit_type": "No Deposit",
                    "customer_type": "Transient",
                    "adr": 120.0,
                    "required_car_parking_spaces": 0,
                    "total_of_special_requests": 1,
                    "lead_time": 50
                }
            ]
        }
    }


class PredictionResponse(BaseModel):
    cancellation_probability: float = Field(..., description="Probability of cancellation (0–1).")
    cancellation_probability_pct: float = Field(..., description="Probability expressed as a percentage.")
    risk_label: Literal["Low", "Moderate", "High"] = Field(..., description="Risk band derived from probability.")
    prediction: int = Field(..., description="Binary prediction: 1 = Cancelled, 0 = Not Cancelled.")


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Root"])
def root():
    """Root endpoint — confirms the API is running."""
    return {"message": "Hotel Intelligence Platform API. See /docs for full API documentation."}


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health():
    """Returns the health status of the API and whether the ML model is loaded."""
    return HealthResponse(
        status="ok" if predictor else "degraded",
        model_loaded=predictor is not None,
        version="1.0.0",
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(booking: BookingFeatures):
    """
    Predict the cancellation probability for a single hotel booking.

    Returns:
    - **cancellation_probability**: float in [0, 1]
    - **cancellation_probability_pct**: same value as a percentage
    - **risk_label**: Low (≤30%), Moderate (30–60%), High (>60%)
    - **prediction**: 0 or 1
    """
    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Model is not loaded. Ensure models/cancellation_model.joblib exists "
                "and restart the server."
            ),
        )

    try:
        df = booking.to_dataframe()
        prob = float(predictor.predict_proba(df)[0])
        pred = int(predictor.predict(df)[0])
    except Exception as exc:
        logger.exception("Prediction failed.")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(exc)}") from exc

    pct = prob * 100
    if pct > 60:
        risk = "High"
    elif pct > 30:
        risk = "Moderate"
    else:
        risk = "Low"

    # ── Audit log (best-effort — never fails the request) ────────────────
    if monitor:
        try:
            monitor.log_prediction(
                features=booking.model_dump(),
                probability=prob,
                risk_label=risk,
                prediction=pred,
            )
        except Exception:  # noqa: BLE001
            logger.warning("Audit log write failed (non-fatal).")

    return PredictionResponse(
        cancellation_probability=round(prob, 4),
        cancellation_probability_pct=round(pct, 2),
        risk_label=risk,
        prediction=pred,
    )


@app.get("/drift", tags=["Monitoring"])
def drift_report():
    """
    Run a drift report comparing live prediction inputs against the
    training distribution. Requires at least a handful of logged predictions.

    Returns:
    - **feature_drift**: PSI score + status for each feature
    - **prediction_drift**: shift in cancellation rate vs reference
    - **overall_status**: stable | moderate_drift | significant_drift
    """
    if monitor is None:
        raise HTTPException(
            status_code=503,
            detail="Drift monitor is not initialised. Check server logs.",
        )
    try:
        return monitor.run_drift_report(min_samples=10)
    except Exception as exc:
        logger.exception("Drift report failed.")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
