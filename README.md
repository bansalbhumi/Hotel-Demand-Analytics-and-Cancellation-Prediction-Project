# 🏨 Hotel Demand Analytics & Cancellation Prediction Platform

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-1798e3?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

An **end-to-end data science and ML engineering portfolio project** transforming raw hotel booking records into a production-ready analytics platform. 

## 🎯 Objective
To build an intelligent, scalable hotel analytics platform that enables revenue and operations managers to understand booking demand, predict and mitigate cancellation risks, optimize dynamic pricing, and derive automated business insights.

## 🚨 Business Problem
Hotels face significant revenue uncertainty and operational inefficiency due to high booking cancellation rates and poor demand forecasting. Management currently relies on manual reporting, which lacks real-time predictive capabilities and fails to accurately segment high-risk customers, leading to unoptimized room rates and empty inventory.

## 💾 Dataset Source
The project utilizes a dataset of 119k+ booking records from two hotel types (City Hotel and Resort Hotel). The data includes booking details such as lead time, length of stay, adults/children, room types, deposit types, and previous cancellation history.

## 🛠️ Tech Stack
- **Data Manipulation & SQL:** Pandas, NumPy, DuckDB
- **Machine Learning:** Scikit-Learn, XGBoost, Optuna
- **Dashboard & Visualization:** Streamlit, Plotly
- **AI Agent Integration:** LangChain, LangGraph, Google Gemini API
- **Deployment & API:** FastAPI, Docker, Docker Compose
- **Testing:** Pytest

## 📁 Folder Structure
```text
Hotel-Demand-Analytics-and-Cancellation-Prediction/
├── api/                       # FastAPI microservice for real-time model inference
├── dashboards/streamlit/      # Streamlit UI (Global filters, analytic views, risk gauge)
├── data/                      # Raw and processed datasets
├── models/                    # Serialized Scikit-Learn pipelines (.joblib)
├── notebooks/                 # Jupyter notebooks (EDA, SQL Analytics, Model Training)
├── presentations/             # Presentation decks and outlines
├── reports/                   # Final project report, model card, insight memos
├── src/                       # Core python modules (feature_engineering, inference, agent)
├── tests/                     # Pytest suite (20+ assertions passing)
├── .env.example               # Environment variables template
├── docker-compose.yml         # Container orchestration
└── README.md
```

## 🚀 Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/bansalbhumi/Hotel-Demand-Analytics-and-Cancellation-Prediction-Project.git
cd Hotel-Demand-Analytics-and-Cancellation-Prediction-Project

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. (Optional) Set up AI Analyst
To use the natural-language SQL Agent, you must provide a free Google Gemini API Key. You can either enter it directly in the Streamlit UI Sidebar, or set it as an environment variable:
```bash
export GOOGLE_API_KEY="your-gemini-key"
```

## 🖥️ How to Run Dashboard
Launch the interactive Streamlit dashboard:
```bash
streamlit run dashboards/streamlit/app.py
```
*The dashboard will automatically open at `http://localhost:8501`*

## 🧪 How to Run Scripts & Tests
You can run the end-to-end automated test suite (checking the API, the ML Pipeline, and data integrity):
```bash
pytest tests/ -v
```
To retrain the ML model from scratch (generates `models/cancellation_model.joblib`):
```bash
python src/model_training.py
```

## 🤖 Model Summary
- **Target:** `is_canceled` (Binary Classification)
- **Algorithm:** XGBoost (Tuned via Optuna) embedded inside a strictly evaluated Scikit-Learn `Pipeline`.
- **Data Leakage Prevention:** Removed all post-booking outcome columns (e.g., `reservation_status`, `assigned_room_type`).
- **Performance:** 
  - **ROC-AUC:** ~0.925
  - **Accuracy:** ~84%
- **Explainability:** Feature importance analysis reveals that *Deposit Type (Non Refund)*, *Lead Time*, and *Country* are the highest drivers of cancellation risk.
- **Reference:** See `reports/model_card.md` for full model documentation.

## 📸 Dashboard Screenshots
*The dashboard features 7 distinct analytic views, including interactive "What-If" prediction simulation and a fully autonomous AI SQL Analyst.*
*(Add your screenshots here)*

## 💡 Key Insights
1. **The 90-Day Cliff:** Cancellation risk rises sharply for bookings made more than 3 months in advance.
2. **The Deposit Paradox:** Counter-intuitively, non-refundable deposits in this dataset show near-100% cancellation rates, driven by erratic bulk corporate group behaviour.
3. **Special Requests as a Commitment Signal:** Guests who make ≥1 special request are significantly *less* likely to cancel.
4. **Stable City, Volatile Resort:** Resort Hotel ADR spikes sharply in summer while City Hotel yields are predictable year-round.

## 📈 Recommendations
- Implement staged confirmation policies and deposit deadlines for bookings with a lead time > 90 days.
- Restructure the "Non Refund" policy for corporate groups to enforce stricter penalties or renegotiate bulk-booking contracts.
- Incentivize personalization (special requests) at the time of booking to increase guest commitment and reduce cancellation probability.
- Apply dynamic pricing algorithms to Resort Hotels during peak summer months to maximize ADR yields.

## ⚠️ Limitations
- The dataset is static historical data; external macro-economic factors (like global pandemics or inflation) are not captured.
- High cancellation rates in the "Non Refund" segment are highly anomalous and likely represent a data-recording artifact specific to this hotel's corporate group handling, which limits generalization to other properties without domain adjustment.

## ✅ Final Deliverables Checklist
- [x] Clean README with objective, setup, usage, findings, limitations
- [x] Cleaned dataset 
- [x] EDA notebook
- [x] SQL analysis notebook (15+ queries)
- [x] Streamlit dashboard with 7 views
- [x] Cancellation model notebook
- [x] Metrics table, confusion matrix, and feature importance visualisations
- [x] Model Card (`reports/model_card.md`)
- [x] Final 5–8 page report (`reports/final_project_report.md`)
- [x] Final 10–12 slide presentation (`presentations/final_project_presentation.md`)
- [x] Stable AI Agent (LangGraph/DuckDB integration)
