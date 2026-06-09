# Week 1 Office Presentation

## Slide 1: Project Overview

Project: Hotel Demand Analytics and Cancellation Prediction

Objective:
- Analyze hotel booking demand.
- Understand cancellation behavior.
- Identify revenue and customer segment patterns.
- Prepare data for dashboard and ML cancellation model.

Dataset:
- Hotel Booking Demand Dataset
- Rows: 119,390
- Original Columns: 32
- Cleaned Columns: 36
- Target Variable: is_canceled

---

## Slide 2: Dataset Structure and Setup

Completed:
- GitHub repository created.
- Folder structure created.
- Kaggle dataset downloaded.
- Virtual environment configured.
- Cleaned dataset saved in data/processed/.

Key files:
- data/raw/hotel_bookings.csv
- data/processed/hotel_bookings_cleaned.csv
- notebooks/01_data_understanding.ipynb
- notebooks/02_visual_analysis.ipynb
- notebooks/04_sql_analytics.ipynb

---

## Slide 3: Data Quality Issues

Missing values found:
- company: 112,593 missing values
- agent: 16,340 missing values
- country: 488 missing values
- children: 4 missing values

Actions taken:
- children filled with 0
- country filled with Unknown
- agent filled with 0
- company filled with 0

Other issues:
- 31,994 duplicate rows found
- ADR contains possible outliers
- Lead time has very high values up to 737 days

---

## Slide 4: First Business Insights

Key findings:
- Overall cancellation rate is 37.04%.
- City Hotel cancellation rate is 41.73%.
- Resort Hotel cancellation rate is 27.76%.
- City Hotels receive 79,330 bookings, almost twice Resort Hotels.
- Non Refund bookings show 99.36% cancellation.
- Transient customers show the highest customer-type cancellation rate at 40.75%.
- Groups market segment shows 61.06% cancellation.
- August has the highest booking volume with 13,877 bookings.

---

## Slide 5: Week 2 Plan

Next work:
- Design dashboard layout.
- Create executive KPI cards.
- Build cancellation dashboard page.
- Build revenue/ADR dashboard page.
- Add filters for hotel, month, market segment, customer type and country.
- Convert charts into business recommendations.

Planned KPIs:
- Total bookings
- Cancellation rate
- Average ADR
- Average lead time
- Total room nights
- Segment share