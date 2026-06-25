# Final Presentation: Hotel Intelligence Platform (HIP)

**Title:** Predicting Demand and Reducing Cancellations  
**Presenter:** Bhumi Bansal  
**Duration:** ~15 Minutes  

---

## Slide 1: Introduction & The Business Problem
- **Context:** The hotel industry operates on thin margins where unpredicted cancellations directly result in lost revenue and wasted operational effort.
- **The Challenge:** While historical data is collected, it is rarely analyzed predictively.
- **The Solution:** The Hotel Intelligence Platform (HIP) — a unified dashboard and AI system to analyze demand, predict individual cancellation risks, and converse with our data.

## Slide 2: Project Architecture
- **Data Layer:** Pandas & DuckDB handle fast, scalable SQL analytics over 119k+ bookings.
- **Machine Learning:** Scikit-Learn (Random Forest) trained to predict the `is_canceled` target variable.
- **Deployment:** FastAPI serves the model, wrapped in Docker containers.
- **Interface:** Streamlit provides the visual BI dashboard and AI Analyst interface.

## Slide 3: Key Insights from Exploratory Data Analysis
- **Seasonality:** Summer months (July & August) account for the highest volume of bookings.
- **Demographics:** A majority of the bookings are originated from European countries, heavily led by Portugal.
- **Lead Time Phenomenon:** The longer the lead time (time between booking and arrival), the significantly higher the chance of cancellation. 

## Slide 4: The Machine Learning Model
- **Algorithm:** Random Forest Classifier was chosen for its interpretability and strong performance.
- **Performance:** Achieved an accuracy of >85%. 
- **Top Predictive Features:**
  - `deposit_type` (Non-Refundable deposits have a high anomaly correlation to cancellations)
  - `country` of origin
  - `lead_time`
  - `total_of_special_requests`

## Slide 5: Explainable AI in Practice
- **The "Black Box" Problem:** Stakeholders need to trust the model. Telling them "it's high risk" isn't enough.
- **SHAP Integration:** The Streamlit dashboard visually explains the top 5 factors driving *every single prediction*. 
- **Value:** Front-desk staff can see exactly *why* a customer might cancel (e.g., "High lead time and no special requests") and proactively offer an incentive.

## Slide 6: AI Data Analyst
- **Beyond Dashboards:** Dashboards answer predefined questions. What about ad-hoc questions?
- **The Agent:** Powered by LangChain and Google Gemini, the AI Analyst allows users to type natural language questions (e.g., *"What is the cancellation rate for groups?"*).
- **Execution:** The agent securely generates SQL, queries DuckDB, and summarizes the result in plain English.

## Slide 7: Production Readiness
- **Dockerized:** The application runs in isolated containers via `docker-compose`.
- **Monitoring & Drift:** Our `monitoring.py` script continuously tracks incoming predictions and calculates the Population Stability Index (PSI) to ensure the model doesn't drift out of relevance.
- **CI/CD:** Automated testing via Pytest ensures API stability.

## Slide 8: Conclusion & Next Steps
- **Impact:** We now have a system that doesn't just look at the past, but anticipates the future.
- **Next Steps:**
  - A/B testing intervention strategies for "High Risk" bookings.
  - Hyperparameter tuning to push accuracy beyond 90%.
  - Integrating live booking feeds directly into the database.

---
*End of Presentation*
