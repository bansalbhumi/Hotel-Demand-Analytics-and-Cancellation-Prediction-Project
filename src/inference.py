import os
import joblib
import pandas as pd
import numpy as np
import logging
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from feature_engineering import BookingFeatureEngineer # Required for unpickling

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CancellationPredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, "..", "models", "cancellation_model.joblib")
            
        logging.info(f"Loading model from {model_path}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please train the model first.")
        
        self.pipeline = joblib.load(model_path)
        
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predicts cancellation (0 = Not Canceled, 1 = Canceled).
        """
        return self.pipeline.predict(data)
        
    def predict_proba(self, data: pd.DataFrame) -> np.ndarray:
        """
        Predicts cancellation probabilities. Returns probability of being canceled.
        """
        return self.pipeline.predict_proba(data)[:, 1]

if __name__ == "__main__":
    # Test inference script
    predictor = CancellationPredictor()
    
    # Dummy raw data test (representing what Streamlit passes)
    test_data = pd.DataFrame([{
        'hotel': 'City Hotel',
        'arrival_date_month': 'August',
        'stays_in_weekend_nights': 1,
        'stays_in_week_nights': 2,
        'adults': 2,
        'children': 0.0,
        'babies': 0,
        'meal': 'BB',
        'country': 'PRT',
        'market_segment': 'Online TA',
        'distribution_channel': 'TA/TO',
        'is_repeated_guest': 0,
        'previous_cancellations': 0,
        'previous_bookings_not_canceled': 0,
        'reserved_room_type': 'A',
        'deposit_type': 'No Deposit',
        'customer_type': 'Transient',
        'adr': 120.50,
        'required_car_parking_spaces': 0,
        'total_of_special_requests': 1,
        'lead_time': 50
    }])
    
    proba = predictor.predict_proba(test_data)
    logging.info(f"Test cancellation probability: {proba[0]:.4f}")
