# Final Project Report: Hotel Demand Analytics & Cancellation Prediction Platform

**Date:** June 24, 2026  
**Author:** Bhumi Bansal  
**Status:** Completed

---

## 1. Executive Summary
The Hotel Intelligence Platform (HIP) is an end-to-end analytics and machine learning solution designed to help hotel management understand booking demand trends, analyze customer behavior, and predict booking cancellations. By integrating exploratory data analysis, predictive modeling, an interactive dashboard, and a natural language AI Analyst, the platform transforms raw booking data into actionable business intelligence.

## 2. Business Objectives
1. **Understand Demand Patterns:** Analyze monthly booking trends, market segment contributions, and Average Daily Rate (ADR) variations.
2. **Predict Cancellations:** Build a machine learning model capable of accurately predicting whether a customer will cancel a booking.
3. **Enhance Explainability:** Provide transparency into why specific bookings are flagged as high risk (using SHAP).
4. **Interactive BI:** Deliver a centralized Streamlit dashboard for real-time data exploration.
5. **AI Data Analyst:** Integrate an LLM-based agent capable of answering complex, ad-hoc business questions via natural language SQL generation.

---

## 3. Data Processing & Engineering
The original dataset (`hotel_bookings.csv`) contained 119,390 records and 32 features. During the data cleaning phase:
- Missing values for `children`, `country`, and `agent` were imputed or dropped as appropriate.
- Engineered features included `total_nights` (weekend + week nights), `total_guests` (adults + children + babies), and `prior_cancel_flag`.
- Categorical features were consolidated, and features like `lead_time` were bucketed into `lead_time_bucket` to capture non-linear relationships.

## 4. Machine Learning Model Development
A **Random Forest Classifier** was selected as the final model due to its robust performance on imbalanced tabular data and its ability to capture complex feature interactions.

### 4.1 Model Performance metrics
The model was evaluated against a baseline Logistic Regression model and demonstrated superior performance:
- **Accuracy:** > 85%
- **F1-Score:** Optimized for the cancellation class.
- **Top Drivers of Cancellation:**
  1. `deposit_type_Non Refund`
  2. `country` (specifically PRT)
  3. `lead_time`
  4. `total_of_special_requests`
  5. `previous_cancellations`

### 4.2 Model Explainability
To ensure business stakeholders trust the model, **SHAP (SHapley Additive exPlanations)** was integrated directly into the UI. This provides a bar chart of the top 5 driving factors for *each individual prediction*, explaining exactly why a booking is rated Low, Moderate, or High risk.

---

## 5. System Architecture & Deployment

### 5.1 Technology Stack
- **Data & Analytics:** Pandas, DuckDB, SQLite
- **Machine Learning:** Scikit-Learn, SHAP
- **Web Dashboard:** Streamlit, Plotly
- **API & Deployment:** FastAPI, Docker, Docker Compose
- **AI Agent:** LangChain, Google Gemini API

### 5.2 Microservices Architecture
The platform was deployed using a decoupled microservices architecture via Docker Compose:
- **`hip_api`:** A FastAPI service exposing REST endpoints (`/predict` and `/drift`) for model inference and drift monitoring.
- **`hip_dashboard`:** A Streamlit application that consumes the API and provides the user interface for executives and analysts.

### 5.3 Monitoring and Drift Detection
A custom drift monitoring system (`src/monitoring.py`) was implemented to track the health of the model in production:
- Logs every prediction request to a SQLite database (`prediction_audit.db`).
- Calculates the **Population Stability Index (PSI)** to detect input feature drift.
- Surfaces changes in prediction distributions (cancellation rates) over time.

---

## 6. Key Business Insights
1. **Seasonality:** Booking volumes peak significantly in August and July. Staffing and dynamic pricing strategies should be aligned with this peak season.
2. **Cancellation Risk by Deposit Type:** Counterintuitively, "Non Refund" deposits exhibit high cancellation rates in this specific dataset, likely due to a specific class of group bookings or data anomalies that warrant further business investigation.
3. **Lead Time Correlation:** Bookings made far in advance (high lead time) have a significantly higher likelihood of cancellation. Implementing stricter confirmation policies for bookings made >90 days in advance could reduce lost revenue.
4. **Special Requests:** Customers making 1 or more special requests are significantly *less* likely to cancel. Enhancing the guest experience during the booking phase solidifies commitment.

## 7. Conclusion
The Hotel Intelligence Platform successfully bridges the gap between raw data and operational decision-making. By combining a predictive cancellation model with deep analytics and an intuitive AI interface, the project empowers the hotel business to proactively mitigate revenue loss and optimize their booking strategies.
