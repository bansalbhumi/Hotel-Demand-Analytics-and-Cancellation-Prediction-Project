"""
Pytest test suite for the Hotel Intelligence Platform.
Covers:
  - src.inference.CancellationPredictor  (model loading + prediction shape)
  - api.main FastAPI routes               (health, predict — valid & invalid)
"""

import sys
import os

import pandas as pd
import pytest
from fastapi.testclient import TestClient

# Make project root importable regardless of how pytest is invoked
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.inference import CancellationPredictor
from api.main import app

# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def predictor():
    return CancellationPredictor()


@pytest.fixture(scope="module")
def sample_df():
    return pd.DataFrame([{
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
        "lead_time": 50,
    }])


@pytest.fixture(scope="module")
def high_risk_df():
    """A booking that should typically score as high-risk."""
    return pd.DataFrame([{
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
        "previous_cancellations": 3,
        "previous_bookings_not_canceled": 0,
        "reserved_room_type": "A",
        "deposit_type": "Non Refund",
        "customer_type": "Transient",
        "adr": 120.0,
        "required_car_parking_spaces": 0,
        "total_of_special_requests": 0,
        "lead_time": 200,
    }])


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# ─────────────────────────────────────────────────────────────────────────────
# Tests: CancellationPredictor
# ─────────────────────────────────────────────────────────────────────────────

class TestCancellationPredictor:

    def test_model_loads(self, predictor):
        """Model pipeline should load without errors."""
        assert predictor.pipeline is not None

    def test_predict_returns_binary(self, predictor, sample_df):
        """predict() should return 0 or 1."""
        result = predictor.predict(sample_df)
        assert len(result) == 1
        assert result[0] in (0, 1)

    def test_predict_proba_in_range(self, predictor, sample_df):
        """predict_proba() should return a float in [0, 1]."""
        prob = predictor.predict_proba(sample_df)[0]
        assert 0.0 <= prob <= 1.0

    def test_high_risk_scores_higher(self, predictor, sample_df, high_risk_df):
        """High-risk booking should have higher cancellation probability."""
        low_prob = predictor.predict_proba(sample_df)[0]
        high_prob = predictor.predict_proba(high_risk_df)[0]
        assert high_prob > low_prob

    def test_predict_multiple_rows(self, predictor, sample_df, high_risk_df):
        """Model should handle a multi-row DataFrame."""
        combined = pd.concat([sample_df, high_risk_df], ignore_index=True)
        probs = predictor.predict_proba(combined)
        assert len(probs) == 2


# ─────────────────────────────────────────────────────────────────────────────
# Tests: FastAPI routes
# ─────────────────────────────────────────────────────────────────────────────

VALID_PAYLOAD = {
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
    "lead_time": 50,
}

HIGH_RISK_PAYLOAD = {
    "hotel": "City Hotel",
    "arrival_date_month": "August",
    "stays_in_weekend_nights": 1,
    "stays_in_week_nights": 2,
    "adults": 2,
    "children": 0,
    "babies": 0,
    "meal": "BB",
    "country": "prt",          # lowercase — validator should uppercase it
    "market_segment": "Online TA",
    "distribution_channel": "TA/TO",
    "is_repeated_guest": 0,
    "previous_cancellations": 3,
    "previous_bookings_not_canceled": 0,
    "reserved_room_type": "A",
    "deposit_type": "Non Refund",
    "customer_type": "Transient",
    "adr": 120.0,
    "required_car_parking_spaces": 0,
    "total_of_special_requests": 0,
    "lead_time": 200,
}


class TestHealthEndpoint:

    def test_health_returns_200(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_health_model_loaded(self, client):
        data = r = client.get("/health").json()
        assert data["model_loaded"] is True
        assert data["status"] == "ok"

    def test_health_version(self, client):
        data = client.get("/health").json()
        assert data["version"] == "1.0.0"


class TestRootEndpoint:

    def test_root_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_root_has_message(self, client):
        data = client.get("/").json()
        assert "message" in data


class TestPredictEndpoint:

    def test_predict_valid_returns_200(self, client):
        r = client.post("/predict", json=VALID_PAYLOAD)
        assert r.status_code == 200

    def test_predict_response_schema(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert "cancellation_probability" in data
        assert "cancellation_probability_pct" in data
        assert "risk_label" in data
        assert "prediction" in data

    def test_predict_probability_in_range(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert 0.0 <= data["cancellation_probability"] <= 1.0

    def test_predict_risk_label_valid(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert data["risk_label"] in ("Low", "Moderate", "High")

    def test_predict_binary_prediction(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert data["prediction"] in (0, 1)

    def test_predict_country_uppercased(self, client):
        """Lowercase country input should still succeed after validator."""
        r = client.post("/predict", json=HIGH_RISK_PAYLOAD)
        assert r.status_code == 200

    def test_predict_high_risk_scores_high(self, client):
        """Non-refund + high lead time + previous cancellations → High risk."""
        data = client.post("/predict", json=HIGH_RISK_PAYLOAD).json()
        assert data["risk_label"] == "High"

    def test_predict_missing_field_returns_422(self, client):
        """Omitting a required field should return HTTP 422 Unprocessable Entity."""
        incomplete = {k: v for k, v in VALID_PAYLOAD.items() if k != "lead_time"}
        r = client.post("/predict", json=incomplete)
        assert r.status_code == 422

    def test_predict_invalid_lead_time_returns_422(self, client):
        """lead_time > 700 is out of range."""
        bad_payload = {**VALID_PAYLOAD, "lead_time": 9999}
        r = client.post("/predict", json=bad_payload)
        assert r.status_code == 422

    def test_predict_invalid_market_segment_returns_422(self, client):
        """Unknown market_segment value should fail validation."""
        bad_payload = {**VALID_PAYLOAD, "market_segment": "Unknown Segment"}
        r = client.post("/predict", json=bad_payload)
        assert r.status_code == 422
