# Technical Requirements Document (TRD)

# Hotel Intelligence Platform (HIP)

Version: 1.0  
Owner: Bhumi Bansal  
Status: Development

---

# 1. System Architecture

User
↓
Streamlit Dashboard
↓
Analytics Layer
↓
Processed Dataset
↓
Machine Learning Layer
↓
Random Forest Model
↓
AI Data Analyst Layer
↓
DuckDB + Pandas Tools

---

# 2. Technology Stack

## Data Layer

- Pandas
- NumPy
- DuckDB
- SQLite

## Visualization

- Streamlit
- Plotly
- Matplotlib

## Machine Learning

- Scikit-Learn
- Logistic Regression
- Random Forest
- Joblib

## AI Layer

- LangChain
- LangGraph
- FastAPI
- Gemini/OpenAI APIs

---

# 3. Repository Structure

```text
Hotel-Demand-Analytics-and-Cancellation-Prediction

├── data
│   ├── raw
│   └── processed
│
├── notebooks
│   ├── 01_data_understanding.ipynb
│   ├── 02_visual_analysis.ipynb
│   └── 03_cancellation_model.ipynb
│
├── src
│   ├── clean_data.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── inference.py
│   ├── utils.py
│   └── config.py
│
├── models
│   └── random_forest.pkl
│
├── dashboards
│   └── streamlit
│       └── app.py
│
├── reports
├── presentations
├── tests
├── requirements.txt
└── README.md
```

---

# 4. Data Pipeline

Raw Dataset

↓

Data Cleaning

↓

Feature Engineering

↓

Train/Test Split

↓

Model Training

↓

Evaluation

↓

Model Serialization

↓

Dashboard Integration

↓

AI Agent

---

# 5. Feature Engineering

## total_nights

weekend nights + week nights

---

## total_guests

adults + children + babies

---

## prior_cancel_flag

previous_cancellations > 0

---

## lead_time_bucket

- 0–30
- 31–90
- 91–180
- 181–400

---

## season

- Winter
- Spring
- Summer
- Autumn

---

# 6. Machine Learning Pipeline

## Baseline Model

Logistic Regression

### Metrics

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

---

## Improved Model

Random Forest

### Parameters

```python
n_estimators=200
max_depth=15
min_samples_split=10
min_samples_leaf=5
max_features='sqrt'
```

---

# 7. Model Explainability

Top Features

1. deposit_type_Non Refund
2. country_PRT
3. lead_time
4. total_of_special_requests
5. previous_cancellations

---

# 8. Dashboard Architecture

## Executive Overview

KPIs

- Total Bookings
- Cancellation Rate
- ADR
- Room Nights

---

## Demand Analysis

- Monthly Trends
- Hotel Comparison

---

## Cancellation Analytics

- Segment Analysis
- Customer Analysis

---

## Pricing Insights

- ADR Distribution
- ADR by Segment

---

## Customer Intelligence

- Country Analysis
- Market Segments

---

## ML Prediction

Risk prediction page

---

## AI Analyst

Natural language interface

---

# 9. AI Agent Architecture

User Query

↓

LLM

↓

Tool Router

↓

SQL Generator

↓

DuckDB

↓

Results

↓

Business Explanation

---

## Tools

### run_read_only_sql()

Executes SELECT statements.

---

### get_kpi()

Returns KPI calculations.

---

### explain_result()

Generates business insights.

---

# 10. Guardrails

Block:

- INSERT
- UPDATE
- DELETE
- DROP
- ALTER

Expose:

- SQL query used
- Data limitations

Never expose:

- API keys
- Credentials

---

# 11. Future Technical Enhancements

## XGBoost

Higher prediction accuracy.

---

## SHAP

Prediction explainability.

---

## Hyperparameter Tuning

GridSearchCV / Optuna.

---

## FastAPI

Model serving.

---

## Docker

Containerization.

---

## GitHub Actions

CI/CD pipelines.

---

## Unit Tests

Pytest-based testing.

---

## Logging

Structured logs.

---

## Monitoring

Model drift detection.

---

## LangGraph

Multi-agent architecture.

---

# 12. Coding Standards

Follow:

- PEP8
- SOLID principles
- Type hints
- Google style guide
- Modular architecture

---

# 13. Deployment Architecture

Client

↓

Streamlit

↓

FastAPI

↓

ML Model

↓

DuckDB

↓

Dataset

---

# 14. Testing

Unit Tests

Integration Tests

Model Validation

Dashboard Testing

AI Agent Testing

Performance Testing

---

# 15. Production Readiness Roadmap

- **Phase 1**: Analytics Platform
- **Phase 2**: Machine Learning
- **Phase 3**: Explainability
- **Phase 4**: AI Agent
- **Phase 5**: FastAPI Deployment
- **Phase 6**: Docker + CI/CD
- **Phase 7**: Monitoring and Drift Detection