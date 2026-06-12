# Hotel-Demand-Analytics-and-Cancellation-Prediction-Project

## OVERVIEW
  This project analyzes hotel booking demand patterns and predicts booking cancellations using machine learning.

## PROJECT OBJECTIVES
  - Analyze booking demand trends
  - Understand cancellation behavior
  - Build interactive dashboards
  - Develop cancellation prediction model
  - Generate business recommendations

## DATASET SOURCE
Dataset: Hotel Booking Demand Dataset

Source:
https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

Main File:
hotel_bookings.csv

Target Variable:
is_canceled


## TECH STACK
  - Python
  - Pandas
  - NumPy
  - DuckDB
  - Scikit-Learn
  - Plotly
  - Streamlit


## INSTALLATION

```bash
git clone <repository-url>
cd Hotel-Demand-Analytics-and-Cancellation-Prediction-Project

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Run Jupyter Notebook:

```bash
jupyter notebook
```

## PROJECT STRUCTURE

```text
Hotel-Demand-Analytics-and-Cancellation-Prediction-Project
│
├── data
│   ├── raw
│   └── processed
│
├── notebooks
│   ├── 01_data_understanding.ipynb
│   ├── 02_visual_analysis.ipynb
│   ├── 03_cancellation_model.ipynb
│   ├── 04_sql_analytics.ipynb
│
├── dashboards
│   ├── dashboard_wireframe.md
│   ├── kpi_definitions.md
│   └── streamlit
│       └── app.py
│
├── reports
├── presentations
├── src
├── requirements.txt
└── README.md
```


## SETUP STATUS

  ## Dataset Information

    | Attribute | Value |
    |------------|---------|
    | File | hotel_bookings.csv |
    | Rows | 119,390 |
    | Columns | 32 |
    | Target Variable | is_canceled |

  ## ENGINEERED FEATURES
    The following features were created during data preprocessing:

    |     Feature       |         Description                  |
    | ----------------- | ------------------------------------ |
    | total_nights      | Total stay duration                  |
    | total_guests      | Adults + Children + Babies           |
    | arrival_month_num | Numeric month representation         |
    | stay_type         | Short Stay / Medium Stay / Long Stay |

---

## BUSINESS QUESTIONS
  1. What are the monthly booking trends?
  2. Which customer segments cancel most frequently?
  3. How does ADR vary across customer types?
  4. What impact does lead time have on cancellations?
  5. Which customer groups are most valuable?
  6. What recommendations can reduce cancellations?

---

## KEY INSIGHTS DISCOVERED

* August recorded the highest booking volume.
* July was the second busiest month.
* Transient customers represent the largest customer segment.
* Portugal contributes the highest number of bookings.
* Resort Hotel guests stay longer on average than City Hotel guests.
* Cancellation behavior varies significantly across customer types.
* Average Daily Rate (ADR) differs by customer segment.
* Lead time appears strongly related to cancellation likelihood.

---

## DASHBOARD PREVIEW
Dashboard development is currently in progress.

Planned Dashboard Pages:
  - Executive Overview
  - Cancellation Analysis
  - ADR & Revenue Analysis
  - Customer Segment Analysis

Dashboard screenshots will be added after completion of Day 8.

---

## PROGRESS

### Week 1 (Day 1 - Day 6)

#### Day 1 - Project Setup

* Repository created
* Folder structure created
* README.md created
* requirements.txt created
* Python virtual environment configured
* Kaggle dataset downloaded
* Dataset verified successfully

#### Day 2 - Data Profiling

* Dataset loaded into Pandas and DuckDB
* Checked dataset dimensions and data types
* Analyzed missing values
* Identified duplicate records
* Performed initial data quality assessment

#### Day 3 - Data Cleaning & Feature Engineering

* Handled missing values
* Created total_nights feature
* Created total_guests feature
* Created arrival_month_num feature
* Created stay_type feature
* Saved cleaned dataset to data/processed

#### Day 4 - SQL Analytics

* Wrote and tested 15+ SQL queries
* Analyzed cancellation rate
* Compared hotel types
* Analyzed ADR trends
* Performed customer segment analysis
* Performed lead-time analysis

#### Day 5 - Office Presentation 1

* Prepared Week 1 presentation
* Summarized dataset structure
* Documented data quality issues
* Presented initial EDA findings
* Presented SQL analysis findings
* Created Week 2 dashboard plan

#### Day 6 - Dashboard Design

##### Dashboard Pages

1. Executive Overview
2. Cancellation Analysis
3. ADR & Revenue Analysis
4. Customer Segment Analysis

##### KPI Definitions

* Total Bookings
* Cancellation Rate
* Average ADR
* Total Room Nights
* Average Lead Time
* Segment Share

##### Global Filters

* Hotel Type
* Arrival Month
* Country
* Market Segment
* Customer Type

##### Deliverables

* Dashboard Wireframe Created
* KPI Definitions Created
* Streamlit Application Skeleton Created

---

## CURRENT PROJECT COMPLETION

Completed Through:
- Day 6 of Internship Plan

Current Phase:
- Dashboard Development

Next Milestone:
- Day 7 Core Visualizations

---

## PROJECT STATUS

### Week 1

* [x] Repository Setup
* [x] Data Profiling
* [x] Data Cleaning
* [x] Feature Engineering
* [x] SQL Analytics
* [x] Week 1 Presentation
* [x] Dashboard Design

### Week 2-3

* [x] Core Visuals
* [x] Interactive Dashboard
* [x] Business Insights
* [ ] Dashboard Presentation

### Week 4-5

* [ ] Feature Engineering for ML
* [ ] Model Training
* [ ] Model Evaluation
* [ ] Model Interpretation

### Week 6

* [ ] Final Report
* [ ] Final Presentation
* [ ] Optional AI Data Analyst Agent
