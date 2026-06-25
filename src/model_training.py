import pandas as pd
import numpy as np
import logging
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

# Import our custom transformer
from feature_engineering import BookingFeatureEngineer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "..", "data", "processed", "hotel_bookings_cleaned.csv")
    model_dir = os.path.join(current_dir, "..", "models")
    
    os.makedirs(model_dir, exist_ok=True)
    
    logging.info(f"Loading cleaned data from {input_path}")
    df = pd.read_csv(input_path)
    
    # We define the target and strictly pre-arrival features to avoid leakage
    target = 'is_canceled'
    
    # Drop known leakage columns if they exist in the dataset
    leakage_cols = ['reservation_status', 'reservation_status_date', 'assigned_room_type', 'booking_changes']
    df = df.drop(columns=[col for col in leakage_cols if col in df.columns], errors='ignore')
    
    # Separate target
    df = df.dropna(subset=[target])
    X = df.drop(columns=[target])
    y = df[target]
    
    logging.info(f"Data shape after removing target/leakage: {X.shape}")
    
    # Stratified split to keep cancellation ratio identical in train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Define which features we will pass to the model AFTER the custom transformer runs
    categorical_features = [
        'hotel', 'meal', 'country', 'market_segment', 'distribution_channel',
        'reserved_room_type', 'deposit_type', 'customer_type',
        'lead_time_bucket', 'season', 'stay_length_bucket'
    ]
    numeric_features = [
        'lead_time', 'total_nights', 'total_guests', 'has_children', 
        'previous_cancellations', 'prior_cancel_flag', 'adr_cleaned', 
        'total_of_special_requests', 'required_car_parking_spaces'
    ]
    
    # Preprocessing for the engineered columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='drop' # Drops any extra columns not specified above
    )
    
    # Build the full master pipeline
    # This pipeline can take a raw single-row DataFrame directly from the Streamlit UI!
    pipeline = Pipeline([
        ('feature_engineer', BookingFeatureEngineer()),
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        ))
    ])
    
    logging.info("Training full ML pipeline...")
    pipeline.fit(X_train, y_train)
    
    logging.info("Evaluating model on test set...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_proba)
    logging.info(f"Final ROC-AUC Score: {auc:.4f}")
    logging.info(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
    
    # Save the unified pipeline
    model_path = os.path.join(model_dir, "cancellation_model.joblib")
    logging.info(f"Saving fully trained pipeline to {model_path}")
    joblib.dump(pipeline, model_path)
    
    logging.info("Pipeline training completed successfully.")

if __name__ == "__main__":
    train()
