# Strategic Asset Management Dashboard: Olist Portfolio Analysis

## Overview
This repository contains a high-performance Strategic Dashboard designed for e-commerce portfolio management. The application utilizes advanced probabilistic models to segment customer databases based on Survival Probability and Projected 12-Month Customer Lifetime Value (CLV).

The core objective of this tool is to transform raw transactional data into actionable business intelligence, allowing stakeholders to optimize resource allocation and regional logistics.

## Core Value Proposition
This tool solves the critical challenge of customer uncertainty in e-commerce. By distinguishing between "active" and "at-risk" customers through BG/NBD models, the business can move from reactive discounting to proactive asset management, directly impacting the bottom line (EBITDA).

## Key Business Insights
* **Pareto Efficiency Concentration:** Analysis reveals that the top 10% of the customer base accounts for nearly 388% of the projected revenue relative to the average, indicating a high-dependency on top-tier assets.
* **Regional Dominance:** São Paulo (SP) and Rio de Janeiro (RJ) represent the core cash flow. Intelligence suggests prioritizing local fulfillment centers in these areas to reduce CAC and improve delivery margins.
* **Capital at Risk:** The dashboard identifies specific revenue amounts currently held by "At-Risk" segments, providing a clear target for reactivation campaigns.

## Strategic Features
* **Asset Matrix:** A visual mapping of Customer Health vs. Financial Value.
* **Segment Roadmaps:** Prescriptive strategies for High-Value, Growth, At-Risk, and Critical Churn segments.
* **Regional Revenue Projection:** Geospatial intelligence for logistics and marketing optimization.

## Technical Stack
* **Framework:** Streamlit
* **Analytics:** Lifetimes (BG/NBD & Gamma-Gamma models), Pandas, Numpy.
* **Visualization:** Plotly Express.
* **Serialization:** Dill (for advanced model persistence).
* **Backend Interface:** FastAPI integration ready.

## Project Structure
* app.py: Core dashboard application.
* data/: Processed RFM and CLV data summaries.
* models/: Serialized predictive models.
* api/: Backend infrastructure for external scaling.
