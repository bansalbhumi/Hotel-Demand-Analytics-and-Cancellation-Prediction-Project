# Model Card: Hotel Cancellation Prediction

## Model Details
- **Model Type:** XGBoost Classifier wrapped in a Scikit-Learn Pipeline
- **Task:** Binary Classification (Predicting whether a booking will be canceled)
- **Target Variable:** `is_canceled` (0 = Not Canceled, 1 = Canceled)

## Intended Use
This model is designed to be used by revenue managers and hotel staff prior to a guest's arrival to estimate the risk of cancellation. This helps hotels optimize their overbooking strategy, forecast revenue more accurately, and proactively engage with high-risk customers.

## Training Data
The model was trained on the `hotel_bookings.csv` dataset, which includes bookings for a City Hotel and a Resort Hotel.

### Preprocessing & Leakage Prevention
To ensure the model is robust and suitable for real-world inference (where future information is unknown), all features representing "post-booking" or "post-arrival" data were strictly excluded. 
**Excluded Features (Leakage Prevention):**
- `reservation_status`
- `reservation_status_date`
- `assigned_room_type`
- `booking_changes`

### Engineered Features
A custom Scikit-Learn Transformer (`BookingFeatureEngineer`) handles engineering automatically:
- `total_nights`: `stays_in_week_nights` + `stays_in_weekend_nights`
- `has_children`: Binary flag indicating presence of children/babies
- `lead_time_bucket`: Categorical bins for lead time
- `stay_length_bucket`: Categorical bins for stay duration
- `prior_cancel_flag`: Binary flag if previous cancellations > 0
- `season`: Derived from arrival month
- `adr_cleaned`: Capped negative ADR at 0, and extreme outliers at 500

## Evaluation Metrics (Test Set)
- **ROC-AUC Score:** 0.9250
- **Overall Accuracy:** 84%
- **Precision (Cancel):** 0.82
- **Recall (Cancel):** 0.73
- **F1-Score (Cancel):** 0.78

## Model Limitations & Cautions
- **Generalization:** This model was trained on historical data specific to two hotels in Portugal. It may not generalize well to hotels in completely different regions, scales, or economic conditions without retraining.
- **Concept Drift:** Factors influencing cancellations (e.g., global pandemics, economic shifts, new travel policies) can change rapidly. The model should be continuously monitored and retrained periodically.
- **Educational Prototype:** This model and its dashboard UI are designed as a portfolio prototype. While technically sound, production deployment would require continuous MLOPs monitoring pipelines.
