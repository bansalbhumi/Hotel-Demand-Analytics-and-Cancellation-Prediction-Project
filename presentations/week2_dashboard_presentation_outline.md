# Week 2 Dashboard Presentation Outline

## Slide 1: Project Overview

### Project

Hotel Demand Analytics and Cancellation Prediction

### Objective

Analyze hotel booking patterns, cancellation behavior, customer segments, and pricing trends using SQL, Python, EDA, and an interactive Streamlit dashboard.

---

## Slide 2: Business Problem

### Challenges

* High booking cancellation rates
* Seasonal demand fluctuations
* Revenue uncertainty
* Dependence on external booking channels

### Goal

Identify important booking patterns and support future cancellation prediction modeling.

---

## Slide 3: Dashboard Overview

### Dashboard Features

* Executive KPI Cards
* Interactive Filters
* Monthly Booking Trends
* Hotel Type Comparison
* Cancellation Analysis
* ADR Analysis
* Market Segment Analysis

### Technology Stack

* Python
* Pandas
* Plotly
* Streamlit
* DuckDB

---

## Slide 4: Key Demand Insights

### Findings

* August recorded the highest booking volume.
* July was the second busiest month.
* City Hotels receive significantly more bookings than Resort Hotels.
* Resort Hotel guests stay longer on average.

### Business Impact

Supports staffing, inventory planning, and pricing optimization.

---

## Slide 5: Cancellation Insights

### Findings

* Overall cancellation rate: 37.04%
* City Hotel cancellation rate: 41.73%
* Transient customers have the highest cancellation risk.
* Lead time strongly influences cancellations.
* Deposit type is highly associated with cancellation behavior.

### Business Impact

Highlights opportunities to improve booking retention.

---

## Slide 6: Revenue and Customer Insights

### Findings

* Transient customers generate the highest ADR.
* Online TA is the largest booking source.
* Portugal contributes the largest share of bookings.
* Most bookings are short-stay reservations.

### Business Impact

Supports customer targeting and revenue optimization.

---

## Slide 7: Next Steps and Project Roadmap

### Machine Learning Phase

- Feature Engineering
- Train-Test Split
- Baseline Model Development
- Model Evaluation
- Cancellation Prediction System

### Key Features Identified

- lead_time
- hotel
- deposit_type
- market_segment
- customer_type
- adr
- previous_cancellations
- total_of_special_requests
- total_nights

### Expected Outcome

Develop a machine learning model capable of predicting booking cancellations and supporting proactive hotel revenue management.
