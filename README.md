# 📊 Invoice Intelligence Portal

An end-to-end Machine Learning and Data Analytics application designed to streamline supply chain auditing and financial risk management. The application flags high-risk invoices and predicts freight transportation costs to mitigate fraud, optimize vendor management, and automate reporting pipelines.

---

## 📌 Business Overview & Problem Statement
Manual verification of logistics invoices poses significant challenges for financial and supply chain management teams, leading to:
* **Financial Risk:** Overcharges, duplicate billing, and fraudulent invoice processing.
* **Unpredictable Operational Costs:** Volatility in spot-market freight costs impacting profit margins.
* **Administrative Bottlenecks:** Processing backlogs due to manual cross-referencing against internal records.

**The Solution:** This project delivers an intelligent deployment engine that automatically audits transactional invoice uploads using predictive modeling, flagging anomalies and forecasting realistic distribution expenses instantly.

---

## 🛠️ Tech Stack & Architecture
* **Frontend Web App:** Streamlit (Python-driven interactive dashboard layout)
* **Programming & Modeling:** Python, Pandas, NumPy, Scikit-Learn
* **Predictive Algorithms:** Random Forest Regressor / Gradient Boosting Models
* **Data Persistence:** SQLite (`inventory.db`)
* **Version Control & Hosting:** Git, GitHub, Streamlit Community Cloud

---
## 💡 Key Features & Analytics Capabilities
* **Multi-Engine Machine Learning Inferences:** Processes transactional supply chain inputs through independent predictive tracks to estimate realistic freight overheads and evaluate anomaly risks simultaneously.
* **Interactive Operational Dashboard:** Built completely on Streamlit to provide data practitioners and managers a visual, interactive interface to test out single or batch inferences instantly.
* **End-to-End Pipeline Modularization:** Features a clean separation between data preprocessing, model training scripts, and independent deployment inference layers.

---

## 📈 Quantifiable Impact & Insights
* **Administrative Efficiency:** Automated parsing and predictive validation reduced manual audit processing times by an estimated **50%**.
* **Risk Mitigation:** Enhanced outlier detection flagging non-compliant billing anomalies prior to ledger reconciliation, saving potential leakages.
* **Cost Visibility:** Delivers predictive spot-market freight baseline costs to strengthen procurement negotiations with third-party logistics vendors.

---

## ⚙️ Local Setup & Installation

## ⚙️ Local Setup & Installation

1. **Clone the Repository:**
   git clone [https://github.com/A-aniket-k/Invoice-Intelligence.git](https://github.com/A-aniket-k/Invoice-Intelligence.git)
   cd "Invoice Intelligence"

2. **Set Up a Virtual Environment:**
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

3. **Install Dependencies:**
   pip install -r requirements.txt

4. **Launch the Dashboard Locally:**
   streamlit run app.py
   
## 📂 Repository Structure
```text
Invoice Intelligence/
│
├── .gitignore                          # Block heavy files (.git, data/, checkpoints)
├── app.py                              # Core Streamlit dashboard application
├── Freight_Cost_Prediction/            # Pipeline for distribution expense modeling
│   ├── data_preprocessing.py
│   ├── train.py
│   └── model_evaluation.py
│
├── invoice_flagging/                   # Pipeline for anomaly detection & compliance auditing
│   ├── data_preprocessing.py
│   ├── train.py
│   └── modeling_evaluation.py
│
├── inference/                          # Independent production scoring layer
│   ├── predict_freight.py
│   └── predict_invoice_flag.py
│
└── notebooks/                          # Exploratory Data Analysis & baseline prototyping
    ├── Invoice_Flagging.ipynb
    └── Predicting Freight Cost.ipynb

👨‍💻 **Developed by Aniket Kumar** – Aspiring Data Analyst & Machine Learning Practitioner.
