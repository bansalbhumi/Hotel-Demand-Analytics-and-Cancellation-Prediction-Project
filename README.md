# 🏨 Hotel Intelligence Platform (HIP)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-1798e3?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

An **end-to-end data science & ML engineering portfolio project** transforming 119 k+ raw hotel booking records into a production-grade, enterprise analytics platform. The platform spans seven development phases — from exploratory data analysis to Docker-containerised microservices and autonomous AI agents.

---

## ✨ Key Features

| Feature | Technology | Highlight |
|---|---|---|
| **Interactive Dashboard** | Streamlit + Plotly | Dark-theme, 6 analytical views, global filters |
| **Cancellation Predictor** | XGBoost + Optuna | **0.93 ROC-AUC**, real-time probability gauge |
| **AI SQL Analyst** | LangChain + Gemini + DuckDB | Natural-language → safe SQL → business insight |
| **REST API** | FastAPI | `/predict` + `/health` + `/drift` endpoints |
| **Drift Monitoring** | PSI + SQLite audit log | Detects feature & prediction shift in production |
| **Docker Compose** | Two-service deployment | `hip_api` + `hip_dashboard` fully containerised |
| **CI-ready Tests** | Pytest | 30+ tests across inference, API, and pipeline |

---

## 📁 Project Structure

```text
Hotel-Demand-Analytics-and-Cancellation-Prediction/
│
├── data/
│   ├── raw/                          # Original 119 k-row CSV
│   └── processed/                    # Cleaned CSV, feature-engineered CSV, SQLite audit DB
│
├── notebooks/
│   ├── 01_data_understanding_and_cleaning.ipynb
│   ├── 02_eda_and_business_insights.ipynb
│   ├── 03_model_training_and_evaluation.ipynb
│   └── 04_sql_analytics.ipynb
│
├── src/
│   ├── data_cleaning.py              # Cleaning pipeline (null-handling, invalid-row removal)
│   ├── feature_engineering.py        # Derived features (total_nights, season, lead_time_bucket…)
│   ├── model_training.py             # Optuna-tuned XGBoost training pipeline
│   ├── inference.py                  # CancellationPredictor wrapper (joblib + sklearn Pipeline)
│   ├── agent.py                      # LangGraph ReAct agent (DuckDB tools + Gemini LLM)
│   └── monitoring.py                 # PSI drift monitor + SQLite audit logger
│
├── api/
│   └── main.py                       # FastAPI app: /predict, /health, /drift
│
├── dashboards/streamlit/
│   ├── app.py                        # Main router + global sidebar filters
│   ├── agent_ui.py                   # AI Analyst chat interface
│   ├── utils/
│   │   ├── theme.py                  # Plotly dark-theme tokens
│   │   └── components.py             # Shared insight card component
│   └── views/
│       ├── executive_overview.py     # KPIs, monthly trend, cancellation split
│       ├── demand_analysis.py        # Seasonality heatmap, monthly booking trend
│       ├── cancellation_analytics.py # Segment and customer type cancellation rates
│       ├── pricing_insights.py       # ADR distribution, ADR by hotel type
│       ├── customer_intelligence.py  # Market segment treemap, country breakdown
│       └── ml_risk_prediction.py     # Live risk gauge, confusion matrix, ROC, feature importance
│
├── models/
│   └── xgboost.pkl                   # Serialised model pipeline (preprocessor + XGBClassifier)
│
├── tests/
│   ├── test_api.py                   # FastAPI endpoint tests (18 assertions)
│   └── test_pipeline.py              # Data-cleaning & feature-engineering unit tests (30+ assertions)
│
├── reports/                          # Business insight memos, model metric CSVs, drift reports
├── presentations/                    # Slide decks and review notes
├── Dockerfile.api                    # Docker image for FastAPI service
├── Dockerfile.dashboard              # Docker image for Streamlit service
├── docker-compose.yml                # Orchestrates both services
├── requirements.txt
├── prd.md                            # Product Requirements Document
└── trd.md                            # Technical Requirements Document
```

---

## 🚀 Getting Started

### Option 1 — Local (venv)

```bash
# 1. Clone and enter the project
git clone https://github.com/bansalbhumi/Hotel-Demand-Analytics-and-Cancellation-Prediction-Project.git
cd Hotel-Demand-Analytics-and-Cancellation-Prediction-Project

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set your Google API key for the AI Analyst tab
#    Windows PowerShell
$env:GOOGLE_API_KEY = "your-gemini-key"
#    macOS / Linux
export GOOGLE_API_KEY="your-gemini-key"
#    Or create a .env file:
echo GOOGLE_API_KEY=your-gemini-key > .env

# 5. Launch the dashboard
streamlit run dashboards/streamlit/app.py
```

> **Note:** The model file (`models/xgboost.pkl`) must exist. If it is missing, re-train it:
> ```bash
> python src/model_training.py
> ```

---

### Option 2 — Docker Compose (recommended for production)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
# Build and start both services
docker-compose up --build

# Services will be available at:
#   Dashboard  →  http://localhost:8501
#   API        →  http://localhost:8000
#   API docs   →  http://localhost:8000/docs
```

Set `GOOGLE_API_KEY` in your shell before running compose, or add it to `docker-compose.yml` under the dashboard service's `environment` block.

---

## 🧪 Running Tests

```bash
# Run the full test suite from the project root
pytest tests/ -v

# Run only the pipeline (data cleaning + feature engineering) tests
pytest tests/test_pipeline.py -v

# Run only the API tests
pytest tests/test_api.py -v
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/`       | Health confirmation |
| `GET`  | `/health` | Model-loaded status + version |
| `POST` | `/predict`| Cancellation probability for a booking |
| `GET`  | `/drift`  | Feature + prediction drift report (PSI) |

**Example `/predict` request:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "deposit_type": "Non Refund",
    "country": "PRT",
    "market_segment": "Online TA",
    "customer_type": "Transient",
    "lead_time": 200,
    "season": "Summer",
    "total_of_special_requests": 0,
    "previous_cancellations": 2,
    "total_nights": 3,
    "total_guests": 2
  }'
```

**Response:**
```json
{
  "cancellation_probability": 0.9712,
  "cancellation_probability_pct": 97.12,
  "risk_label": "High",
  "prediction": 1
}
```

---

## 📊 Key Business Insights

- **The 90-Day Cliff** — Cancellation risk rises sharply for bookings made more than 3 months in advance. Implementing staged confirmation policies for long-horizon bookings could recover significant revenue.
- **The Deposit Paradox** — Counter-intuitively, non-refundable deposits in this dataset show near-100% cancellation rates, driven by erratic bulk corporate group behaviour — a signal worth investigating with the reservations team.
- **Special Requests as Commitment Signal** — Guests who make ≥1 special request are significantly *less* likely to cancel. Encouraging personalisation at booking time is a low-cost retention lever.
- **Stable City, Volatile Resort** — Resort Hotel ADR spikes sharply in summer while City Hotel yields are predictable year-round — suggesting different dynamic pricing strategies for each property type.

---

## 🗺️ Development Phases

| Phase | Scope | Status |
|-------|-------|--------|
| 1 | Exploratory Data Analysis + SQL Analytics | ✅ Complete |
| 2 | Machine Learning (XGBoost + Optuna) | ✅ Complete |
| 3 | Explainability (Feature Importance + SHAP) | ✅ Complete |
| 4 | AI Data Analyst Agent (LangGraph + Gemini) | ✅ Complete |
| 5 | FastAPI REST API | ✅ Complete |
| 6 | Docker Compose Deployment | ✅ Complete |
| 7 | Drift Monitoring + Audit Logging | ✅ Complete |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Data** | Pandas, NumPy, DuckDB, SQLite |
| **ML** | Scikit-Learn, XGBoost, SHAP, Optuna |
| **Visualisation** | Streamlit, Plotly |
| **AI Agent** | LangChain, LangGraph, Google Gemini |
| **API** | FastAPI, Uvicorn, Pydantic |
| **Deployment** | Docker, Docker Compose |
| **Testing** | Pytest |

---

## 👩‍💻 Author

**Bhumi Bansal** — Data Science & ML Engineering Portfolio Project
