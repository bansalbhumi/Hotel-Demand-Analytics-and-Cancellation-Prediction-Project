import pandas as pd
import numpy as np
import logging
import os
from sklearn.base import BaseEstimator, TransformerMixin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BookingFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom Scikit-Learn Transformer to engineer features for hotel booking data.
    Ensures that identical transformations are applied during training and inference.
    """
    def __init__(self):
        self.season_map = {
            'December': 'Winter', 'January': 'Winter', 'February': 'Winter',
            'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
            'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
            'September': 'Autumn', 'October': 'Autumn', 'November': 'Autumn'
        }

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # We work on a copy to avoid SettingWithCopyWarning
        df = X.copy()
        
        def safe_get(col_name, default_val=0):
            if col_name not in df.columns:
                return pd.Series(default_val, index=df.index)
            return df[col_name].fillna(default_val)
        
        # 1. total_nights
        if 'total_nights' not in df.columns:
            df['total_nights'] = safe_get('stays_in_weekend_nights') + safe_get('stays_in_week_nights')
        
        # 2. total_guests
        if 'total_guests' not in df.columns:
            df['total_guests'] = safe_get('adults', 2) + safe_get('children', 0) + safe_get('babies', 0)
            
        # 3. has_children
        df['has_children'] = ((safe_get('children') + safe_get('babies')) > 0).astype(int)
        
        # 4. prior_cancel_flag
        if 'prior_cancel_flag' not in df.columns:
            df['prior_cancel_flag'] = (safe_get('previous_cancellations') > 0).astype(int)
            
        # 5. lead_time_bucket
        if 'lead_time_bucket' not in df.columns:
            bins = [-1, 30, 90, 180, 1000]
            labels = ['0-30', '31-90', '91-180', '181+']
            df['lead_time_bucket'] = pd.cut(safe_get('lead_time'), bins=bins, labels=labels).astype(str)
            
        # 6. stay_length_bucket
        if 'stay_length_bucket' not in df.columns:
            stay_bins = [-1, 2, 7, 14, 100]
            stay_labels = ['Short (0-2)', 'Medium (3-7)', 'Long (8-14)', 'Very Long (15+)']
            df['stay_length_bucket'] = pd.cut(df['total_nights'], bins=stay_bins, labels=stay_labels).astype(str)
            
        # 7. season
        if 'season' not in df.columns and 'arrival_date_month' in df.columns:
            df['season'] = df['arrival_date_month'].map(self.season_map).fillna('Summer')
            
        # 8. adr_cleaned
        if 'adr' in df.columns:
            # Cap negative ADR at 0
            df['adr_cleaned'] = df['adr'].clip(lower=0.0)
            # Cap high outliers at 500
            df['adr_cleaned'] = df['adr_cleaned'].clip(upper=500.0)
        else:
            df['adr_cleaned'] = 100.0 # fallback default if totally missing
            
        return df

if __name__ == "__main__":
    # Test script for the transformer
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "..", "data", "processed", "hotel_bookings_cleaned.csv")
    
    logging.info(f"Loading cleaned data from {input_path}")
    df_clean = pd.read_csv(input_path, nrows=100) # test on sample
    
    engineer = BookingFeatureEngineer()
    df_features = engineer.transform(df_clean)
    
    logging.info(f"Engineered columns: {df_features.columns.tolist()}")
    logging.info("Process finished successfully.")
