import pytest
import pandas as pd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.inference import CancellationPredictor

@pytest.fixture(scope="module")
def predictor():
    return CancellationPredictor()

def test_low_risk_booking(predictor):
    data = pd.DataFrame([{
        'hotel': 'Resort Hotel',
        'arrival_date_month': 'January',
        'stays_in_weekend_nights': 1,
        'stays_in_week_nights': 1,
        'adults': 2,
        'children': 0,
        'babies': 0,
        'meal': 'BB',
        'country': 'PRT',
        'market_segment': 'Direct',
        'distribution_channel': 'Direct',
        'is_repeated_guest': 1,
        'previous_cancellations': 0,
        'previous_bookings_not_canceled': 2,
        'reserved_room_type': 'A',
        'deposit_type': 'No Deposit',
        'customer_type': 'Transient',
        'adr': 50.0,
        'required_car_parking_spaces': 1,
        'total_of_special_requests': 2,
        'lead_time': 5
    }])
    
    prob = predictor.predict_proba(data)[0]
    assert prob < 0.30, f"Expected low risk, got {prob:.2f}"

def test_high_risk_booking(predictor):
    data = pd.DataFrame([{
        'hotel': 'City Hotel',
        'arrival_date_month': 'August',
        'stays_in_weekend_nights': 2,
        'stays_in_week_nights': 5,
        'adults': 2,
        'children': 0,
        'babies': 0,
        'meal': 'BB',
        'country': 'PRT',
        'market_segment': 'Online TA',
        'distribution_channel': 'TA/TO',
        'is_repeated_guest': 0,
        'previous_cancellations': 2,
        'previous_bookings_not_canceled': 0,
        'reserved_room_type': 'A',
        'deposit_type': 'Non Refund',
        'customer_type': 'Transient',
        'adr': 250.0,
        'required_car_parking_spaces': 0,
        'total_of_special_requests': 0,
        'lead_time': 300
    }])
    
    prob = predictor.predict_proba(data)[0]
    assert prob > 0.60, f"Expected high risk, got {prob:.2f}"
