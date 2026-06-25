"""
Pytest test suite — src.data_cleaning & src.feature_engineering
Hotel Intelligence Platform (HIP)

Covers:
  - data_cleaning.clean_data()   : null-handling, zero-guest removal, dtype preservation
  - feature_engineering.engineer_features() : derived column correctness, bucketing, season map
"""

import sys
import os

import numpy as np
import pandas as pd
import pytest

# Ensure project root is on the path regardless of invocation directory
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.data_cleaning import clean_data
from src.feature_engineering import BookingFeatureEngineer


# ─────────────────────────────────────────────────────────────────────────────
# Shared fixtures
# ─────────────────────────────────────────────────────────────────────────────

def _minimal_raw_row(**overrides) -> dict:
    """Return a minimal, valid raw-row dict that mirrors the hotel_bookings schema."""
    base = {
        "hotel": "City Hotel",
        "is_canceled": 0,
        "lead_time": 50,
        "arrival_date_year": 2017,
        "arrival_date_month": "July",
        "arrival_date_week_number": 27,
        "arrival_date_day_of_month": 1,
        "stays_in_weekend_nights": 1,
        "stays_in_week_nights": 2,
        "adults": 2,
        "children": None,   # deliberately null
        "babies": 0,
        "meal": "BB",
        "country": None,    # deliberately null
        "market_segment": "Online TA",
        "distribution_channel": "TA/TO",
        "is_repeated_guest": 0,
        "previous_cancellations": 0,
        "previous_bookings_not_canceled": 0,
        "reserved_room_type": "A",
        "assigned_room_type": "A",
        "booking_changes": 0,
        "deposit_type": "No Deposit",
        "agent": None,      # deliberately null
        "company": None,    # deliberately null
        "days_in_waiting_list": 0,
        "customer_type": "Transient",
        "adr": 100.0,
        "required_car_parking_spaces": 0,
        "total_of_special_requests": 1,
        "reservation_status": "Check-Out",
        "reservation_status_date": "2017-07-04",
    }
    base.update(overrides)
    return base


@pytest.fixture
def raw_df():
    """A small DataFrame with 3 clean rows and 1 zero-guest row."""
    rows = [
        _minimal_raw_row(adults=2),
        _minimal_raw_row(adults=1, children=1.0),
        _minimal_raw_row(adults=1),
        _minimal_raw_row(adults=0, children=None, babies=0),  # zero-guest — must be removed
    ]
    return pd.DataFrame(rows)


@pytest.fixture
def cleaned_df(raw_df):
    return clean_data(raw_df)


@pytest.fixture
def engineered_df(cleaned_df):
    return BookingFeatureEngineer().fit_transform(cleaned_df.copy())


# ─────────────────────────────────────────────────────────────────────────────
# Tests: data_cleaning.clean_data()
# ─────────────────────────────────────────────────────────────────────────────

class TestCleanData:

    def test_removes_zero_guest_rows(self, raw_df, cleaned_df):
        """Rows where adults + children + babies == 0 must be dropped."""
        assert len(cleaned_df) == len(raw_df) - 1

    def test_children_nulls_filled_with_zero(self, cleaned_df):
        """Null children values should be replaced with 0."""
        assert cleaned_df["children"].isna().sum() == 0
        assert (cleaned_df["children"] == 0).any()

    def test_country_nulls_filled_with_unknown(self, cleaned_df):
        """Null country values should become 'Unknown'."""
        assert cleaned_df["country"].isna().sum() == 0
        assert (cleaned_df["country"] == "Unknown").any()

    def test_agent_nulls_filled_with_zero(self, cleaned_df):
        """Null agent values should be replaced with 0."""
        assert cleaned_df["agent"].isna().sum() == 0

    def test_company_nulls_filled_with_zero(self, cleaned_df):
        """Null company values should be replaced with 0."""
        assert cleaned_df["company"].isna().sum() == 0

    def test_output_is_dataframe(self, cleaned_df):
        assert isinstance(cleaned_df, pd.DataFrame)

    def test_original_columns_preserved(self, raw_df, cleaned_df):
        """All original columns must still be present after cleaning."""
        for col in raw_df.columns:
            assert col in cleaned_df.columns

    def test_valid_rows_not_removed(self, cleaned_df):
        """Rows with at least 1 guest should survive cleaning."""
        total_guests = cleaned_df["adults"] + cleaned_df["children"] + cleaned_df["babies"]
        assert (total_guests > 0).all()

    def test_idempotent(self, cleaned_df):
        """Running clean_data twice should produce the same result."""
        double_cleaned = clean_data(cleaned_df.copy())
        assert len(double_cleaned) == len(cleaned_df)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: feature_engineering.engineer_features()
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineerFeatures:

    def test_total_nights_computed(self, engineered_df):
        """total_nights = stays_in_weekend_nights + stays_in_week_nights."""
        expected = (
            engineered_df["stays_in_weekend_nights"]
            + engineered_df["stays_in_week_nights"]
        )
        pd.testing.assert_series_equal(
            engineered_df["total_nights"].reset_index(drop=True),
            expected.reset_index(drop=True),
            check_names=False,
        )

    def test_total_guests_computed(self, engineered_df):
        """total_guests = adults + children + babies."""
        expected = (
            engineered_df["adults"]
            + engineered_df["children"]
            + engineered_df["babies"]
        )
        pd.testing.assert_series_equal(
            engineered_df["total_guests"].reset_index(drop=True),
            expected.reset_index(drop=True),
            check_names=False,
        )

    def test_prior_cancel_flag_zero_when_no_cancellations(self, engineered_df):
        """prior_cancel_flag must be 0 when previous_cancellations == 0."""
        no_prior = engineered_df[engineered_df["previous_cancellations"] == 0]
        assert (no_prior["prior_cancel_flag"] == 0).all()

    def test_prior_cancel_flag_one_when_cancellations_exist(self):
        """prior_cancel_flag must be 1 when previous_cancellations > 0."""
        row = _minimal_raw_row(adults=2, previous_cancellations=2)
        df = BookingFeatureEngineer().fit_transform(clean_data(pd.DataFrame([row])))
        assert df["prior_cancel_flag"].iloc[0] == 1

    # --- lead_time_bucket ---

    @pytest.mark.parametrize("lead_time,expected_bucket", [
        (0,   "0-30"),
        (30,  "0-30"),
        (31,  "31-90"),
        (90,  "31-90"),
        (91,  "91-180"),
        (180, "91-180"),
        (181, "181+"),
        (500, "181+"),
    ])
    def test_lead_time_bucket_boundaries(self, cleaned_df, lead_time, expected_bucket):
        """Lead-time bucketing should assign correct bucket at every boundary."""
        df = cleaned_df.copy()
        df["lead_time"] = lead_time
        df = BookingFeatureEngineer().fit_transform(df)
        assert str(df["lead_time_bucket"].iloc[0]) == expected_bucket

    # --- season ---

    @pytest.mark.parametrize("month,expected_season", [
        ("January",   "Winter"),
        ("February",  "Winter"),
        ("December",  "Winter"),
        ("March",     "Spring"),
        ("April",     "Spring"),
        ("May",       "Spring"),
        ("June",      "Summer"),
        ("July",      "Summer"),
        ("August",    "Summer"),
        ("September", "Autumn"),
        ("October",   "Autumn"),
        ("November",  "Autumn"),
    ])
    def test_season_mapping_all_months(self, cleaned_df, month, expected_season):
        """Season should be correctly derived for every month of the year."""
        df = cleaned_df.copy()
        df["arrival_date_month"] = month
        df = BookingFeatureEngineer().fit_transform(df)
        assert df["season"].iloc[0] == expected_season

    def test_new_columns_added(self, engineered_df):
        """All five engineered columns must be present in the output."""
        for col in ["total_nights", "total_guests", "prior_cancel_flag",
                    "lead_time_bucket", "season"]:
            assert col in engineered_df.columns, f"Missing column: {col}"

    def test_output_length_unchanged(self, cleaned_df, engineered_df):
        """Feature engineering must not add or drop rows."""
        assert len(engineered_df) == len(cleaned_df)
