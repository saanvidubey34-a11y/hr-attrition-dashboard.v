# PulseHR: Workforce Analytics & Employee Attrition Predictor Dashboard

A modern, production-ready, interactive Human Resource Analytics and Employee Attrition Prediction platform. Built with Python, Streamlit, Scikit-Learn, and Plotly.

---

## 🌟 Project Overview

Employee turnover is one of the most expensive challenges facing modern enterprises, incurring direct recruitment expenses, lost institutional knowledge, and team morale decay. **PulseHR** combines descriptive workforce business intelligence with predictive machine learning to empower HR leaders to identify flight risks early and implement targeted, data-backed retention interventions.

---

## 🚀 Key Features

### 1. Modern SaaS UI & Responsive Experience
- **Enterprise Design System**: Modern color palette (Slate, Indigo, Emerald, Amber, Crimson), high-contrast typography, and subtle card elevation with box shadows.
- **Custom Hero Banner**: Executive header summarizing purpose and organizational health context.
- **Live Visual KPI Cards**: Top-level metric cards tracking Total Headcount, Attrition Rate (%), Average Monthly Income, Average Job Satisfaction, and OverTime Load with status pills.

### 2. Synthetic HR Dataset Generator (`numpy` Seeded)
- Generates 1,200 realistic, statistically coherent employee records with a fixed random seed (`seed=42`) for reproducibility.
- Features: `EmployeeID`, `Age`, `Department`, `JobRole`, `MonthlyIncome`, `JobSatisfaction`, `YearsAtCompany`, `OverTime`, and `Attrition`.
- Realistic behavioral correlations: Churn likelihood modeled using logistic log-odds reflecting real-world attrition drivers (overtime pressure, compensation disparities, early-career vulnerability, and satisfaction decay).

### 3. Real-Time Dynamic Sidebar Filters
- **Department**: Multi-select filter across Research & Development, Sales, and Human Resources.
- **OverTime Status**: Toggle between overtime contributors and standard-hour workers.
- **Monthly Income Slider**: Dynamic range slider ($2,400 to $20,000) updating all charts, metrics, and data tables in real time.

### 4. Interactive Workforce Insights (Plotly)
- **Departmental Attrition Dynamics**: Grouped comparative bar charts tracking headcount and turnover volume.
- **Monthly Income vs. Attrition**: Notched statistical box plots displaying compensation disparity between retained and departed employees.
- **Job Satisfaction Correlation**: Bar chart analyzing attrition rate across satisfaction tiers (1 to 4).
- **Tenure & Workload Distribution**: Multi-dimensional scatter plot correlating years at company, monthly income, overtime status, and attrition flags.
- **HRM Strategic Takeaways**: Executive analytical takeaways highlighting turnover patterns.

### 5. Attrition Risk Predictor (Scikit-Learn Machine Learning)
- **Random Forest Classifier**: Pre-trained supervised ensemble model (`n_estimators=120`, `max_depth=6`, balanced class weights) with an integrated OneHotEncoder preprocessing pipeline.
- **Interactive Simulation Form**: Real-time evaluation of an employee's profile (Age, Years at Company, OverTime, Monthly Income, Job Satisfaction).
- **Probabilistic Risk Gauge**: Visual radial gauge indicating low (<30%), moderate (30–60%), or high (>60%) flight risk.
- **Feature Importance Inspector**: Expandable visualization showing the top predictive drivers of attrition.
- **Dynamic Actionable HR Interventions**: Contextual retention strategies generated in response to individual risk factors (workload redistribution, compensation adjustments, skip-level check-ins, early-tenure mentoring).

### 6. Raw Employee Records & Advanced Talent Search
- **Multi-Field Smart Search**: Real-time keyword search across Employee ID, Job Role, and Department.
- **Talent Facet Filters**: Filter by Attrition Status (Active / Exited), Job Role, Job Satisfaction level, and Tenure range.
- **Custom Sorting**: Sort results by Monthly Income, Tenure, Job Satisfaction, Age, or Employee ID in ascending/descending order.
- **Real-Time Cohort Metrics**: Instant KPI summary displaying matching talent count, cohort attrition rate, average salary, and sentiment for the filtered group.
- **Individual Employee 360° Profile Inspector**: Select any individual employee to inspect their compensation, tenure, and calculate their real-time ML flight risk probability.
- **One-Click CSV Export**: Instant report generation via `Export Searched Cohort to CSV` for offline review and HR meetings.
- **Descriptive Statistics**: Collapsible summary breakdown of all numerical metrics.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.9+ (Tested on Python 3.11)
- **Web Framework**: Streamlit
- **Data Manipulation**: Pandas, NumPy
- **Interactive Visualizations**: Plotly Express & Plotly Graph Objects
- **Machine Learning**: Scikit-Learn (Random Forest Classifier, Pipeline, ColumnTransformer, OneHotEncoder)

---

## 📦 Installation & Setup

### 1. Clone or Navigate to the Project Directory
```bash
cd hr-attrition-dashboard
```

### 2. (Optional but Recommended) Create a Virtual Environment
```bash
# Using standard Python venv
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

*Alternatively, if using `uv`:*
```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*Or using `uv`:*
```bash
uv pip install -r requirements.txt
```

---

## ▶️ Running the Application

Launch the Streamlit web dashboard:
```bash
streamlit run app.py
```

The application will open automatically in your browser at:
```
http://localhost:8501
```

---

## 📂 Project Structure

```
hr-attrition-dashboard/
│
├── app.py                # Main Streamlit web application & ML pipeline
├── requirements.txt      # Project Python dependencies
└── README.md             # Project documentation & HRM methodology
```

---

## 📚 Strategic HRM Principles & Retention Framework

This platform operationalizes core Human Resource Management principles:
1. **Herzberg's Two-Factor Theory**: Differentiating hygiene factors (salary, workload/overtime) from motivators (job satisfaction, career advancement).
2. **Predictive Talent Analytics**: Transitioning HR from reactive exit interviews to proactive, data-driven retention forecasting.
3. **Turnover Cost Mitigation**: Identifying early-tenure vulnerability (0–2 years) to protect recruitment and onboarding ROI.
4. **Targeted Interventions**: Recommending tailored management actions rather than one-size-fits-all retention policies.
