# Strategic Asset Management Dashboard | Olist Portfolio

## 📊 Overview
This project is a high-level **Strategic Dashboard** designed for e-commerce asset management. Using advanced probabilistic models, it segments customers based on their **Survival Probability** and **Projected 12-Month Customer Lifetime Value (CLV)**.

The goal is to provide actionable business intelligence to optimize marketing spend and regional logistics.

## 🚀 Key Features
* **Asset Matrix:** Visualization of Portfolio Health vs. Financial Value.
* **Strategic Segmentation:** Automated classification into High-Value, Growth, At-Risk, and Critical Churn assets.
* **Regional Intelligence:** Geospatial analysis identifying revenue density and market leaders (e.g., SP and RJ).
* **Prescriptive Roadmaps:** Data-driven recommendations for each segment to reduce CAC and increase EBITDA.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Data Science:** Lifetimes (BG/NBD & Gamma-Gamma models), Pandas, Numpy.
* **Visualization:** Plotly Express.
* **Serialization:** Dill (for complex model persistence).
* **Backend:** FastAPI (ready for production scaling).

## 📂 Project Structure
* `app.py`: Main dashboard application.
* `data/`: Contains processed RFM and CLV summaries.
* `models/`: Serialized predictive models (.dill).
* `api/`: Backend endpoints for external integration.

## 📈 Business Insights
Based on current data, the **Top 10% of customers** drive a significant portion of projected revenue. Optimization in the **São Paulo (SP)** region is recommended to maximize logistics efficiency.
