# Week 2 Insight Memo - Hotel Demand Analytics Dashboard

## Project

Hotel Demand Analytics and Cancellation Prediction

## Objective

This memo supports Day 9 of the internship plan: translating dashboard findings into management actions.
It converts SQL analysis, EDA findings, and dashboard observations into business insights and practical hotel management recommendations.

---

## Key Business Insights

### 1. Overall cancellation risk is high

Out of 119,390 total bookings, 44,224 bookings were cancelled. The overall cancellation rate is 37.04%.

#### Business Interpretation
More than one-third of reservations are cancelled before check-in, which creates uncertainty in occupancy planning, staffing, and revenue forecasting.

#### Management Action
Develop a cancellation-risk monitoring system and use early warning indicators such as lead time, customer type, deposit type, and market segment.

---

### 2. City Hotels have higher demand but higher cancellation exposure

City Hotels account for approximately 66.45% of total bookings, while Resort Hotels account for 33.55%. City Hotels also have a higher cancellation rate of 41.73%, compared to 27.76% for Resort Hotels.

#### Business Interpretation
City Hotels generate stronger demand but face greater booking instability.

#### Management Action
City Hotels should use stricter confirmation reminders, controlled overbooking policies, and targeted retention strategies for high-risk bookings.

---

### 3. Resort Hotels have longer stays

Resort Hotel guests stay an average of 4.32 nights, while City Hotel guests stay an average of 2.98 nights.

#### Business Interpretation
Resort Hotels appear to attract longer leisure-oriented stays, while City Hotels are more associated with short-duration trips.

#### Management Action
Resort Hotels should promote long-stay packages, vacation bundles, and loyalty offers.

---

### 4. Lead time is strongly associated with cancellation

Cancelled bookings have an average lead time of approximately 145 days, while non-cancelled bookings have an average lead time of approximately 80 days.

#### Business Interpretation
Customers booking far in advance are more likely to cancel, possibly because their plans are less fixed.

#### Management Action
Use lead-time-based reminders, pre-arrival confirmations, and re-engagement campaigns for bookings made far in advance.

---

### 5. Deposit type is one of the strongest cancellation indicators

Non Refund bookings show a cancellation rate of 99.36%. Out of 14,587 Non Refund bookings, 14,494 were cancelled. No Deposit bookings show a cancellation rate of 28.38%, while Refundable bookings show 22.22%. 
This behavior appears counterintuitive because non-refundable reservations are generally expected to reduce cancellations. The field should be investigated further during data validation.

#### Business Interpretation
Deposit type has a very strong relationship with cancellation behavior. However, the unusually high cancellation rate for Non Refund bookings should be interpreted carefully and investigated further.

#### Management Action
Review how deposit policies are recorded and used operationally before making strict business decisions based only on this field.

---

### 6. Market segment affects cancellation behavior

The Groups market segment bookings show the highest cancellation rate at 61.06%. Online Travel Agency bookings show a cancellation rate of 36.72%, while Direct bookings are more reliable with a cancellation rate of 15.34%. 
Online TA contributes 56,477 bookings (47.3% of all reservations).

#### Business Interpretation
Booking channel and market segment strongly influence cancellation risk.

#### Management Action
Hotels should encourage direct bookings using loyalty benefits, exclusive offers, and lower-friction booking experiences.

---

### 7. Transient customers are high-value but high-risk

Transient customers account for 89,613 bookings and have the highest customer-type cancellation rate at 40.75%. They also generate the highest average ADR at 107.01.

#### Business Interpretation
Transient customers are financially valuable but less reliable.

#### Management Action
Use personalized follow-ups, targeted offers, and confirmation reminders for transient customers to reduce cancellation risk.

---

### 8. Group customer type is more reliable

Group customers have the lowest customer-type cancellation rate at 10.23%.

#### Business Interpretation
Organized group customers are more stable than individual transient customers.

#### Management Action
Hotels can prioritize group relationships for predictable occupancy and stable revenue planning.

---

### 9. Demand is highly seasonal

August records the highest booking volume with 13,877 bookings, followed by July with 12,661 bookings. January records the lowest demand with 5,929 bookings.

#### Business Interpretation
Hotel demand increases significantly during the summer season.

#### Management Action
Hotels should adjust staffing, pricing, room inventory, and marketing campaigns ahead of July and August.

---

### 10. Portugal is the dominant customer market

Portugal contributes 48,590 bookings, approximately 40.7% of all reservations, making it the dominant customer market. The United Kingdom and France are the next largest markets.

#### Business Interpretation
The hotel business depends heavily on Portuguese domestic demand.

#### Management Action
Maintain strong domestic marketing while also expanding international acquisition campaigns in the UK, France, and other underrepresented markets.

---

### 11. Short stays dominate hotel demand

Short Stay reservations account for 76,454 bookings, which is approximately 64% of total bookings.

#### Business Interpretation
Most hotel demand comes from short-duration trips.

#### Management Action
Hotels should optimize room turnover, housekeeping schedules, and short-stay pricing packages.

---

### 12. Stay duration alone is not a major cancellation driver

Short Stay bookings have a cancellation rate of 37.70%, Medium Stay bookings 35.90%, and Long Stay bookings 35.74%.

#### Business Interpretation
Cancellation rates do not vary strongly across stay-duration categories.

#### Management Action
Stay duration should be used as a supporting feature, not as the main cancellation-risk indicator.

---

## Final Business Recommendations

1. Prioritize cancellation-risk monitoring for City Hotels.
2. Use lead-time-based reminders for bookings made far in advance.
3. Encourage direct bookings to reduce dependency on high-risk external channels.
4. Create targeted retention campaigns for Transient customers.
5. Review deposit-type behavior carefully before using it for operational policy.
6. Prepare staffing and pricing strategies before July-August peak demand.
7. Promote long-stay packages for Resort Hotels.
8. Use dashboard filters regularly to monitor hotel type, customer type, market segment, country, and deposit-type performance.

---

## Model Development Considerations

Based on the analysis, the following variables should be prioritized during cancellation prediction model development:

- lead_time
- hotel
- deposit_type
- market_segment
- customer_type
- adr
- previous_cancellations
- total_of_special_requests
- country
- total_nights

These variables show strong business relevance and should be tested during feature engineering and model training.

---

## Conclusion

The analysis shows that hotel cancellations are mainly influenced by lead time, hotel type, deposit type, market segment, and customer type. City Hotels generate higher demand and ADR but also face higher cancellation risk. Transient customers and long-lead-time bookings require special monitoring. These findings justify the next phase of the project: building a cancellation prediction model.