import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import io

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="PulseHR | Talent Analytics & Attrition Predictor",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# HTML Render Helper (Guarantees zero raw-code leakage)
# ---------------------------------------------------------
def render_html(html_str: str):
    """
    Renders HTML cleanly in Streamlit without markdown whitespace/indentation interference.
    Strips leading indentation from each line to prevent Markdown from interpreting
    indented HTML lines as indented code blocks (<pre><code>).
    """
    cleaned = "\n".join([line.strip() for line in html_str.strip().splitlines() if line.strip()])
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        st.markdown(cleaned, unsafe_allow_html=True)


# ---------------------------------------------------------
# Custom Modern SaaS CSS Theme
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }

    /* Hero Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        border-radius: 16px;
        padding: 2rem 2.2rem;
        color: #ffffff;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        top: -40%;
        right: -10%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(99, 102, 241, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        background: rgba(99, 102, 241, 0.25);
        border: 1px solid rgba(165, 180, 252, 0.3);
        border-radius: 9999px;
        color: #c7d2fe;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    .hero-title {
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin: 0 0 0.4rem 0;
        color: #ffffff !important;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        color: #94a3b8 !important;
        margin: 0;
        max-width: 780px;
        line-height: 1.5;
    }

    /* Metric card styling enhancements */
    div[data-testid="stMetric"] {
        padding: 0.4rem 0.2rem;
    }

    div[data-testid="stMetric"] label {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #64748b;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }

    /* Sidebar Brand Styling */
    .sidebar-brand {
        padding: 0.5rem 0 1.2rem 0;
        border-bottom: 1px solid rgba(226, 232, 240, 0.4);
        margin-bottom: 1.2rem;
    }

    .sidebar-brand-name {
        font-size: 1.2rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-brand-caption {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 2px;
    }

    /* Recommendation Alert Card */
    .rec-box {
        background: rgba(99, 102, 241, 0.06);
        border-left: 4px solid #4f46e5;
        border-radius: 0 10px 10px 0;
        padding: 0.85rem 1.1rem;
        margin-bottom: 0.75rem;
    }

    .rec-title {
        font-weight: 700;
        font-size: 0.88rem;
        margin-bottom: 0.2rem;
    }

    .rec-desc {
        font-size: 0.82rem;
        line-height: 1.45;
        margin: 0;
        opacity: 0.9;
    }

    /* =========================================================
       Sleek Sidebar & Controls Overrides (Aesthetic Indigo Theme)
       ========================================================= */
    section[data-testid="stSidebar"] {
        background-color: #0c101c !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 0.8rem !important;
    }

    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] label span {
        font-size: 0.83rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        letter-spacing: 0.01em !important;
    }

    /* Multi-select tag chips: replace harsh coral-red with refined indigo pills */
    section[data-testid="stSidebar"] span[data-baseweb="tag"],
    span[data-baseweb="tag"] {
        background-color: rgba(99, 102, 241, 0.16) !important;
        border: 1px solid rgba(165, 180, 252, 0.35) !important;
        border-radius: 6px !important;
        color: #e0e7ff !important;
        padding: 2px 8px !important;
        font-weight: 500 !important;
        font-size: 0.78rem !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] span,
    span[data-baseweb="tag"] span {
        color: #e0e7ff !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] svg,
    span[data-baseweb="tag"] svg {
        fill: #a5b4fc !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"]:hover,
    span[data-baseweb="tag"]:hover {
        background-color: rgba(99, 102, 241, 0.28) !important;
        border-color: rgba(165, 180, 252, 0.6) !important;
    }

    /* Select input boxes */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
        border-color: #6366f1 !important;
    }

    /* Slider Track, Thumbs, and Value Labels */
    section[data-testid="stSidebar"] div[data-testid="stSlider"] [role="slider"] {
        background-color: #6366f1 !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.6) !important;
        width: 16px !important;
        height: 16px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stTickBar"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSlider"] [data-baseweb="slider"] div {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stSliderTickBarMin"],
    section[data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stSliderTickBarMax"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
    }

    /* Radio buttons container in sidebar */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        background-color: #111827;
        padding: 6px 10px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        gap: 8px;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label span {
        color: #cbd5e1 !important;
        font-size: 0.82rem !important;
    }
</style>
"""
render_html(CUSTOM_CSS)


# ---------------------------------------------------------
# Synthetic HR Dataset Generator
# ---------------------------------------------------------
@st.cache_data
def generate_hr_dataset(n_samples: int = 1200, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates a realistic, statistically coherent synthetic HR employee dataset
    with fixed random seed for reproducibility across HRM analytics and ML.
    """
    rng = np.random.default_rng(random_seed)

    dept_roles = {
        "Research & Development": [
            "Research Scientist",
            "Laboratory Technician",
            "Software Engineer",
            "Research Director",
            "Healthcare Representative"
        ],
        "Sales": [
            "Sales Executive",
            "Sales Representative",
            "Sales Manager"
        ],
        "Human Resources": [
            "HR Executive",
            "HR Specialist",
            "HR Manager"
        ]
    }

    departments = rng.choice(
        ["Research & Development", "Sales", "Human Resources"],
        size=n_samples,
        p=[0.58, 0.34, 0.08]
    )

    job_roles = [rng.choice(dept_roles[d]) for d in departments]

    # Age: Normal distribution centered around 37 (range 21-60)
    ages = np.clip(rng.normal(loc=37, scale=8.5, size=n_samples).astype(int), 21, 60)

    # Years at Company: Realistic bounded tenure
    max_possible_tenure = np.maximum(ages - 18, 1)
    years_at_company = np.array([
        rng.integers(0, min(m, 28)) for m in max_possible_tenure
    ])

    # OverTime flag (~28% overtime rate)
    overtime = rng.choice(["Yes", "No"], size=n_samples, p=[0.28, 0.72])

    # Job Satisfaction: 1 (Low) to 4 (Very High)
    satisfaction = rng.choice([1, 2, 3, 4], size=n_samples, p=[0.18, 0.28, 0.32, 0.22])

    # Monthly Income: Base calculated from role hierarchy + tenure bonus + age factor + noise
    role_base_salary = {
        "Sales Representative": 3100,
        "Laboratory Technician": 3600,
        "HR Specialist": 3900,
        "Research Scientist": 5200,
        "HR Executive": 5600,
        "Sales Executive": 6400,
        "Software Engineer": 7200,
        "Healthcare Representative": 7800,
        "HR Manager": 12500,
        "Sales Manager": 13800,
        "Research Director": 15400
    }

    monthly_incomes = []
    for role, tenure, age in zip(job_roles, years_at_company, ages):
        base = role_base_salary.get(role, 5000)
        tenure_bonus = tenure * 240
        age_bonus = (age - 21) * 85
        noise = rng.normal(0, 450)
        income = int(np.clip(base + tenure_bonus + age_bonus + noise, 2400, 19800))
        monthly_incomes.append(income)
    monthly_incomes = np.array(monthly_incomes)

    # Compute realistic attrition probability using logistic function based on key HR risk factors
    z = (
        - 1.45
        + (overtime == "Yes") * 1.35
        - (satisfaction - 2.5) * 0.75
        - ((monthly_incomes - 6500) / 4000) * 0.65
        - ((ages - 37) / 10) * 0.40
        + (years_at_company <= 2) * 0.60
        + (years_at_company >= 12) * 0.20
        + rng.normal(0, 0.45, size=n_samples)
    )
    attrition_probs = 1 / (1 + np.exp(-z))
    attrition = np.where(attrition_probs > 0.50, "Yes", "No")

    df = pd.DataFrame({
        "EmployeeID": [f"EMP-{1001 + i}" for i in range(n_samples)],
        "Age": ages,
        "Department": departments,
        "JobRole": job_roles,
        "MonthlyIncome": monthly_incomes,
        "JobSatisfaction": satisfaction,
        "YearsAtCompany": years_at_company,
        "OverTime": overtime,
        "Attrition": attrition
    })

    return df


# Load base dataset
raw_df = generate_hr_dataset()


# ---------------------------------------------------------
# Sidebar Navigation & Advanced Filter Controls
# ---------------------------------------------------------
with st.sidebar:
    render_html("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-name">
                <span>🏢</span> PulseHR Suite
            </div>
            <div class="sidebar-brand-caption">Workforce Intelligence & Retention Engine</div>
        </div>
    """)

    st.subheader("Filter Workforce")

    all_departments = sorted(raw_df["Department"].unique().tolist())
    selected_departments = st.multiselect(
        "🏢 Department",
        options=all_departments,
        default=all_departments,
        help="Filter employee cohorts by operational business unit"
    )

    ot_choice = st.radio(
        "⏱️ OverTime Commitment",
        options=["All Employees", "OverTime Active (Yes)", "Standard Hours (No)"],
        index=0,
        help="Filter staff by overtime profile"
    )
    if ot_choice == "OverTime Active (Yes)":
        selected_overtime = ["Yes"]
    elif ot_choice == "Standard Hours (No)":
        selected_overtime = ["No"]
    else:
        selected_overtime = ["Yes", "No"]

    min_inc = int(raw_df["MonthlyIncome"].min())
    max_inc = int(raw_df["MonthlyIncome"].max())
    selected_income_range = st.slider(
        "💵 Monthly Income Range ($)",
        min_value=min_inc,
        max_value=max_inc,
        value=(min_inc, max_inc),
        step=250,
        format="$%d"
    )

    if st.button("↺ Reset All Filters", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.caption("PulseHR Intelligence Suite • Enterprise Edition")


# ---------------------------------------------------------
# Apply Real-Time Dynamic Filters
# ---------------------------------------------------------
filtered_df = raw_df[
    (raw_df["Department"].isin(selected_departments)) &
    (raw_df["OverTime"].isin(selected_overtime)) &
    (raw_df["MonthlyIncome"] >= selected_income_range[0]) &
    (raw_df["MonthlyIncome"] <= selected_income_range[1])
].copy()


# ---------------------------------------------------------
# Hero Header Banner
# ---------------------------------------------------------
render_html("""
    <div class="hero-banner">
        <div class="hero-badge">⚡ Human Capital Intelligence Platform</div>
        <h1 class="hero-title">Strategic HR Analytics & Attrition Predictor</h1>
        <p class="hero-subtitle">
            Leverage enterprise-grade workforce behavioral data, descriptive attrition metrics,
            and predictive machine learning to proactively identify retention risks and enhance employee lifetime value.
        </p>
    </div>
""")


# ---------------------------------------------------------
# Top-Level Executive KPI Metric Cards
# ---------------------------------------------------------
total_headcount = len(filtered_df)
baseline_headcount = len(raw_df)

if total_headcount > 0:
    attrited_count = len(filtered_df[filtered_df["Attrition"] == "Yes"])
    attrition_rate = (attrited_count / total_headcount) * 100
    avg_income = filtered_df["MonthlyIncome"].mean()
    avg_satisfaction = filtered_df["JobSatisfaction"].mean()
    ot_percentage = (len(filtered_df[filtered_df["OverTime"] == "Yes"]) / total_headcount) * 100

    sat_label = "Optimal" if avg_satisfaction >= 3.0 else ("Moderate" if avg_satisfaction >= 2.3 else "Needs Focus")
else:
    attrited_count = 0
    attrition_rate = 0.0
    avg_income = 0.0
    avg_satisfaction = 0.0
    ot_percentage = 0.0
    sat_label = "N/A"

# Render KPIs using native containers & metrics to guarantee seamless light/dark mode and zero code rendering bugs
kpi_c1, kpi_c2, kpi_c3, kpi_c4, kpi_c5 = st.columns(5)

with kpi_c1:
    with st.container(border=True):
        st.metric(
            label="Total Headcount",
            value=f"{total_headcount:,}",
            delta=f"{(total_headcount / baseline_headcount * 100):.1f}% of org" if baseline_headcount else None,
            delta_color="off"
        )

with kpi_c2:
    with st.container(border=True):
        st.metric(
            label="Attrition Rate",
            value=f"{attrition_rate:.1f}%",
            delta=f"{attrited_count:,} Exited Staff",
            delta_color="inverse" if attrition_rate >= 15 else "normal"
        )

with kpi_c3:
    with st.container(border=True):
        st.metric(
            label="Avg. Monthly Income",
            value=f"${avg_income:,.0f}",
            delta="Per Employee / Mo",
            delta_color="off"
        )

with kpi_c4:
    with st.container(border=True):
        st.metric(
            label="Avg. Job Satisfaction",
            value=f"{avg_satisfaction:.2f} / 4.0",
            delta=sat_label,
            delta_color="normal" if avg_satisfaction >= 2.5 else "inverse"
        )

with kpi_c5:
    with st.container(border=True):
        st.metric(
            label="OverTime Load",
            value=f"{ot_percentage:.1f}%",
            delta="Overtime Ratio",
            delta_color="inverse" if ot_percentage >= 30 else "off"
        )

st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Main Tabs Navigation
# ---------------------------------------------------------
tab_insights, tab_predictor, tab_data = st.tabs([
    "📊 Workforce Insights & Analytics",
    "🎯 Attrition Risk Predictor (ML)",
    "📁 Raw Employee Records & Export"
])


# =========================================================
# TAB 1: WORKFORCE INSIGHTS
# =========================================================
with tab_insights:
    if total_headcount == 0:
        st.warning("⚠️ No employee records match your selected sidebar filters. Please broaden your filter criteria.")
    else:
        # Row 1: Department-wise Attrition & Monthly Income Distribution
        c1, c2 = st.columns(2)

        with c1:
            with st.container(border=True):
                st.subheader("🏢 Departmental Attrition Dynamics")
                st.caption("Volume of active vs exited talent across organizational divisions")

                dept_summary = (
                    filtered_df.groupby(["Department", "Attrition"])
                    .size()
                    .reset_index(name="Count")
                )

                fig_dept = px.bar(
                    dept_summary,
                    x="Department",
                    y="Count",
                    color="Attrition",
                    barmode="group",
                    color_discrete_map={"No": "#4f46e5", "Yes": "#f43f5e"},
                    labels={"Count": "Headcount", "Department": "Business Unit"},
                    text="Count"
                )
                fig_dept.update_traces(textposition="outside", marker_line_width=0)
                fig_dept.update_layout(
                    margin=dict(l=20, r=20, t=25, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans", size=12),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)"),
                    height=340
                )
                st.plotly_chart(fig_dept, use_container_width=True)

        with c2:
            with st.container(border=True):
                st.subheader("💰 Monthly Income vs. Attrition Status")
                st.caption("Compensation variance between retained staff and departed employees")

                fig_inc = px.box(
                    filtered_df,
                    x="Attrition",
                    y="MonthlyIncome",
                    color="Attrition",
                    color_discrete_map={"No": "#10b981", "Yes": "#f43f5e"},
                    points="outliers",
                    labels={"MonthlyIncome": "Monthly Income ($)", "Attrition": "Attrition Flag"},
                    notched=True
                )
                fig_inc.update_layout(
                    margin=dict(l=20, r=20, t=25, b=20),
                    showlegend=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans", size=12),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)"),
                    height=340
                )
                st.plotly_chart(fig_inc, use_container_width=True)

        # Row 2: Job Satisfaction Distribution & Tenure vs OverTime
        c3, c4 = st.columns(2)

        with c3:
            with st.container(border=True):
                st.subheader("⭐ Job Satisfaction & Churn Correlation")
                st.caption("Attrition proportion across 1-4 employee satisfaction rating tiers")

                sat_map = {1: "1 - Low", 2: "2 - Medium", 3: "3 - High", 4: "4 - Very High"}
                df_sat = filtered_df.copy()
                df_sat["SatisfactionLevel"] = df_sat["JobSatisfaction"].map(sat_map)

                sat_stats = df_sat.groupby(["SatisfactionLevel", "Attrition"]).size().unstack(fill_value=0)
                if "Yes" in sat_stats.columns:
                    sat_stats["AttritionRate"] = (sat_stats["Yes"] / (sat_stats["Yes"] + sat_stats.get("No", 0))) * 100
                else:
                    sat_stats["AttritionRate"] = 0.0
                sat_stats = sat_stats.reset_index()

                fig_sat = px.bar(
                    sat_stats,
                    x="SatisfactionLevel",
                    y="AttritionRate",
                    text=sat_stats["AttritionRate"].apply(lambda v: f"{v:.1f}%"),
                    labels={"SatisfactionLevel": "Satisfaction Score", "AttritionRate": "Attrition Rate (%)"},
                    color="AttritionRate",
                    color_continuous_scale="Reds"
                )
                fig_sat.update_traces(textposition="outside", marker_line_width=0)
                fig_sat.update_layout(
                    margin=dict(l=20, r=20, t=25, b=20),
                    coloraxis_showscale=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans", size=12),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)", range=[0, max(sat_stats["AttritionRate"].max() * 1.25, 10)]),
                    height=340
                )
                st.plotly_chart(fig_sat, use_container_width=True)

        with c4:
            with st.container(border=True):
                st.subheader("⏱️ Tenure vs. Flight Risk by OverTime")
                st.caption("Impact of company tenure (years) and overtime workload on employee churn")

                fig_tenure = px.scatter(
                    filtered_df,
                    x="YearsAtCompany",
                    y="MonthlyIncome",
                    color="Attrition",
                    symbol="OverTime",
                    color_discrete_map={"No": "#6366f1", "Yes": "#f43f5e"},
                    opacity=0.75,
                    labels={"YearsAtCompany": "Tenure at Company (Years)", "MonthlyIncome": "Monthly Income ($)"},
                    hover_data=["JobRole", "Age", "JobSatisfaction"]
                )
                fig_tenure.update_layout(
                    margin=dict(l=20, r=20, t=25, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans", size=12),
                    xaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)"),
                    yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)"),
                    height=340
                )
                st.plotly_chart(fig_tenure, use_container_width=True)

        # HRM Strategic Summary Callout
        with st.container(border=True):
            st.markdown("#### 💡 HRM Executive Strategic Takeaways")
            st.markdown("""
            - **Workload Factor:** Employees clocking mandatory Overtime exhibit significantly elevated attrition probability compared to their standard-hour peers.
            - **Compensation Benchmark:** Departed team members show a lower median income tier, emphasizing the necessity for routine compensation parity reviews.
            - **Tenure Fragility:** Turnover frequency peaks within the first 0–2 years of organizational tenure, signifying an opportunity to strengthen early-tenure employee onboarding and mentorship programs.
            """)


# =========================================================
# TAB 2: ATTRITION RISK PREDICTOR (SCIKIT-LEARN ML)
# =========================================================
with tab_predictor:
    @st.cache_resource
    def train_attrition_model(data: pd.DataFrame):
        feature_cols = ["Age", "MonthlyIncome", "JobSatisfaction", "YearsAtCompany", "OverTime"]
        X = data[feature_cols].copy()
        y = (data["Attrition"] == "Yes").astype(int)

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), ["OverTime"])
            ],
            remainder="passthrough"
        )

        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=120,
                max_depth=6,
                min_samples_split=4,
                random_state=42,
                class_weight="balanced"
            ))
        ])

        pipeline.fit(X, y)
        return pipeline, feature_cols

    model_pipeline, model_features = train_attrition_model(raw_df)

    with st.container(border=True):
        st.subheader("🎯 Individual Employee Attrition Risk Predictor")
        st.caption("Configure talent parameters to compute real-time flight risk probabilities using an ensemble Random Forest algorithm, complete with actionable HRM retention interventions.")

    col_form, col_result = st.columns([1.1, 1.0])

    with col_form:
        with st.container(border=True):
            st.markdown("#### 📝 Employee Profile Input")
            st.caption("Adjust employee profile metrics to simulate retention probability")

            with st.form("attrition_simulation_form"):
                f_col1, f_col2 = st.columns(2)

                with f_col1:
                    input_age = st.slider("Employee Age", min_value=18, max_value=65, value=34, step=1)
                    input_tenure = st.slider("Years at Company", min_value=0, max_value=30, value=3, step=1)
                    input_overtime = st.selectbox("OverTime Status", options=["No", "Yes"], index=1)

                with f_col2:
                    input_income = st.slider(
                        "Monthly Income ($)",
                        min_value=2000,
                        max_value=20000,
                        value=4800,
                        step=250,
                        format="$%d"
                    )
                    input_sat = st.select_slider(
                        "Job Satisfaction Score",
                        options=[1, 2, 3, 4],
                        value=2,
                        format_func=lambda x: {1: "1 - Low", 2: "2 - Medium", 3: "3 - High", 4: "4 - Very High"}[x]
                    )

                submit_btn = st.form_submit_button("⚡ Predict Attrition Risk", use_container_width=True, type="primary")

        # Feature Importance Insights
        with st.expander("🔍 View Model Feature Weights & Top Attrition Drivers", expanded=False):
            rf_model = model_pipeline.named_steps["classifier"]
            feat_names = ["OverTime (Yes)", "Age", "Monthly Income", "Job Satisfaction", "Years at Company"]
            importances = rf_model.feature_importances_

            fi_df = pd.DataFrame({"Feature": feat_names, "Importance": importances}).sort_values(by="Importance", ascending=True)

            fig_fi = px.bar(
                fi_df,
                x="Importance",
                y="Feature",
                orientation="h",
                color="Importance",
                color_continuous_scale="Purples",
                labels={"Importance": "Gini Feature Weight", "Feature": "Predictor Variable"}
            )
            fig_fi.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=240,
                coloraxis_showscale=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans", size=11),
                xaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)"),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_fi, use_container_width=True)

    with col_result:
        sample_input = pd.DataFrame({
            "Age": [input_age],
            "MonthlyIncome": [input_income],
            "JobSatisfaction": [input_sat],
            "YearsAtCompany": [input_tenure],
            "OverTime": [input_overtime]
        })

        probs = model_pipeline.predict_proba(sample_input)[0]
        attrition_prob = probs[1] * 100

        if attrition_prob < 30.0:
            risk_tier = "Low Flight Risk"
            gauge_color = "#10b981"
            risk_icon = "🟢"
        elif attrition_prob < 60.0:
            risk_tier = "Moderate Flight Risk"
            gauge_color = "#f59e0b"
            risk_icon = "🟡"
        else:
            risk_tier = "High Flight Risk"
            gauge_color = "#f43f5e"
            risk_icon = "🔴"

        with st.container(border=True):
            st.markdown(f"#### {risk_icon} Assessment: {risk_tier} ({attrition_prob:.1f}%)")
            st.caption("Probabilistic turnover forecast produced by calibrated Random Forest")

            # Radial Gauge Visualization
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=attrition_prob,
                number={"suffix": "%", "font": {"family": "Plus Jakarta Sans", "size": 36}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar": {"color": gauge_color, "thickness": 0.28},
                    "bgcolor": "rgba(148, 163, 184, 0.1)",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 30], "color": "rgba(16, 185, 129, 0.15)"},
                        {"range": [30, 60], "color": "rgba(245, 158, 11, 0.15)"},
                        {"range": [60, 100], "color": "rgba(244, 63, 94, 0.15)"}
                    ],
                    "threshold": {
                        "line": {"color": gauge_color, "width": 3},
                        "thickness": 0.75,
                        "value": attrition_prob
                    }
                }
            ))
            fig_gauge.update_layout(
                margin=dict(l=25, r=25, t=20, b=10),
                height=210,
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans")
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown("##### Recommended Retention Interventions")

            recs = []
            if input_overtime == "Yes":
                recs.append((
                    "⚖️ Work-Life Balance & Overtime Mitigation",
                    "Overtime is an acute turnover catalyst. Undertake workload rebalancing, assess task delegation, and offer flexible working arrangements or compensatory leave."
                ))
            if input_sat <= 2:
                recs.append((
                    "🤝 Sentiment & Career Check-In",
                    "Job satisfaction score indicates disengagement. Conduct a structured 1-on-1 skip-level meeting to identify friction points and discuss internal career progression."
                ))
            if input_income < 5500:
                recs.append((
                    "💵 Compensation Benchmarking",
                    "Monthly income lies within the bottom compensation percentiles. Review internal salary bands and benchmark against regional industry averages to avoid talent poaching."
                ))
            if input_tenure <= 2:
                recs.append((
                    "🌱 Onboarding & Early-Tenure Mentorship",
                    "Early tenure (<2 years) exhibits structural vulnerability to turnover. Assign a senior peer mentor and establish milestone check-ins at 60 and 90 days."
                ))
            if input_age < 30 and input_tenure > 3:
                recs.append((
                    "🚀 High-Potential Growth Path",
                    "Young talent with established organizational tenure responds well to sponsored certifications, lateral rotation, and accelerated leadership pathways."
                ))

            if not recs:
                recs.append((
                    "✨ Sustained Engagement Maintenance",
                    "Employee profile reflects stable retention markers. Maintain positive engagement cadence, provide continuous recognition, and review annual growth milestones."
                ))

            for title, desc in recs:
                render_html(f"""
                    <div class="rec-box">
                        <div class="rec-title">{title}</div>
                        <p class="rec-desc">{desc}</p>
                    </div>
                """)


# =========================================================
# TAB 3: RAW EMPLOYEE DATA & MANAGEMENT
# =========================================================
with tab_data:
    with st.container(border=True):
        st.subheader("📁 Employee Records Directory & Advanced Talent Search")
        st.caption("Search across records, apply granular cohort filters, inspect individual 360° talent risk profiles, and export custom HR reports.")

        # Top Search Bar & Primary Actions
        search_col, sort_col, sort_dir_col = st.columns([2.5, 1.2, 0.8])

        with search_col:
            search_query = st.text_input(
                "🔎 Quick Search Directory",
                placeholder="Search by Employee ID (e.g. EMP-1050), Job Role, or Department...",
                label_visibility="collapsed"
            )

        with sort_col:
            sort_field = st.selectbox(
                "Sort by",
                options=["MonthlyIncome", "YearsAtCompany", "JobSatisfaction", "Age", "EmployeeID"],
                format_func=lambda x: {
                    "MonthlyIncome": "💵 Monthly Income",
                    "YearsAtCompany": "⏱️ Tenure (Years)",
                    "JobSatisfaction": "⭐ Job Satisfaction",
                    "Age": "🎂 Age",
                    "EmployeeID": "🆔 Employee ID"
                }[x],
                label_visibility="collapsed"
            )

        with sort_dir_col:
            sort_order = st.selectbox(
                "Order",
                options=["Descending", "Ascending"],
                label_visibility="collapsed"
            )

        # Advanced Filter Facets Expander
        with st.expander("⚙️ Advanced Search Filters & Talent Facets", expanded=True if search_query else False):
            f1, f2, f3, f4 = st.columns(4)

            with f1:
                attrition_filter = st.selectbox(
                    "Attrition Status",
                    options=["All Employees", "Active Only (No)", "Exited Only (Yes)"]
                )

            with f2:
                available_roles = sorted(filtered_df["JobRole"].unique().tolist())
                role_filter = st.multiselect(
                    "Job Roles",
                    options=available_roles,
                    default=[],
                    placeholder="All Roles"
                )

            with f3:
                sat_filter = st.multiselect(
                    "Job Satisfaction",
                    options=[1, 2, 3, 4],
                    default=[],
                    format_func=lambda x: {1: "1 - Low", 2: "2 - Medium", 3: "3 - High", 4: "4 - Very High"}[x],
                    placeholder="All Satisfaction Levels"
                )

            with f4:
                min_tenure = int(filtered_df["YearsAtCompany"].min()) if len(filtered_df) > 0 else 0
                max_tenure = int(filtered_df["YearsAtCompany"].max()) if len(filtered_df) > 0 else 30
                tenure_filter = st.slider(
                    "Tenure at Company (Years)",
                    min_value=min_tenure,
                    max_value=max_tenure if max_tenure > min_tenure else min_tenure + 1,
                    value=(min_tenure, max_tenure if max_tenure > min_tenure else min_tenure + 1)
                )

        # Apply Search and Facet Filtering
        display_df = filtered_df.copy()

        # 1. Text Search across multiple columns
        if search_query:
            query = search_query.strip().lower()
            display_df = display_df[
                display_df["EmployeeID"].str.lower().contains(query) |
                display_df["JobRole"].str.lower().contains(query) |
                display_df["Department"].str.lower().contains(query)
            ]

        # 2. Attrition Status Filter
        if attrition_filter == "Active Only (No)":
            display_df = display_df[display_df["Attrition"] == "No"]
        elif attrition_filter == "Exited Only (Yes)":
            display_df = display_df[display_df["Attrition"] == "Yes"]

        # 3. Role Filter
        if role_filter:
            display_df = display_df[display_df["JobRole"].isin(role_filter)]

        # 4. Satisfaction Filter
        if sat_filter:
            display_df = display_df[display_df["JobSatisfaction"].isin(sat_filter)]

        # 5. Tenure Filter
        display_df = display_df[
            (display_df["YearsAtCompany"] >= tenure_filter[0]) &
            (display_df["YearsAtCompany"] <= tenure_filter[1])
        ]

        # 6. Sorting
        ascending = (sort_order == "Ascending")
        display_df = display_df.sort_values(by=sort_field, ascending=ascending)

        # Cohort Live Summary Metrics
        if len(display_df) > 0:
            c_att = len(display_df[display_df["Attrition"] == "Yes"])
            c_rate = (c_att / len(display_df)) * 100
            c_salary = display_df["MonthlyIncome"].mean()
            c_sat = display_df["JobSatisfaction"].mean()

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Matching Talent", f"{len(display_df):,}", f"{(len(display_df)/len(raw_df)*100):.1f}% of total org", delta_color="off")
            with m2:
                st.metric("Cohort Attrition Rate", f"{c_rate:.1f}%", f"{c_att} exited staff", delta_color="inverse" if c_rate >= 15 else "normal")
            with m3:
                st.metric("Cohort Avg. Income", f"${c_salary:,.0f}", "Monthly base")
            with m4:
                st.metric("Cohort Satisfaction", f"{c_sat:.2f} / 4.0", "Cohort sentiment")
        else:
            st.warning("⚠️ No employee records match your combined search keywords and facet criteria.")

        # Export & Table Header
        header_l, header_r = st.columns([2, 1])
        with header_l:
            st.caption(f"Showing **{len(display_df):,}** results of **{len(filtered_df):,}** filtered records ({len(raw_df):,} total company records).")
        with header_r:
            csv_buffer = io.StringIO()
            display_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            st.download_button(
                label="📥 Export Searched Cohort to CSV",
                data=csv_data,
                file_name="HR_Talent_Search_Report.csv",
                mime="text/csv",
                use_container_width=True,
                help="Download clean CSV report of currently searched/filtered employees"
            )

        # Rich Dataframe Display
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "EmployeeID": st.column_config.TextColumn("Employee ID", help="Unique identifier"),
                "Age": st.column_config.NumberColumn("Age", format="%d yrs"),
                "Department": st.column_config.TextColumn("Department"),
                "JobRole": st.column_config.TextColumn("Job Role"),
                "MonthlyIncome": st.column_config.NumberColumn("Monthly Income", format="$%d"),
                "JobSatisfaction": st.column_config.ProgressColumn(
                    "Job Satisfaction",
                    min_value=1,
                    max_value=4,
                    format="%d/4"
                ),
                "YearsAtCompany": st.column_config.NumberColumn("Tenure", format="%d yrs"),
                "OverTime": st.column_config.TextColumn("Overtime"),
                "Attrition": st.column_config.TextColumn("Attrition Flag")
            }
        )

        # Individual Employee 360° Profile Inspector
        if len(display_df) > 0:
            with st.expander("👤 Inspect Individual Employee 360° Profile", expanded=False):
                emp_options = display_df["EmployeeID"].tolist()
                selected_emp_id = st.selectbox(
                    "Select Employee ID to inspect profile & flight risk:",
                    options=emp_options,
                    format_func=lambda eid: f"{eid} — {display_df[display_df['EmployeeID']==eid]['JobRole'].values[0]} ({display_df[display_df['EmployeeID']==eid]['Department'].values[0]})"
                )

                if selected_emp_id:
                    emp_row = display_df[display_df["EmployeeID"] == selected_emp_id].iloc[0]
                    emp_input = pd.DataFrame({
                        "Age": [emp_row["Age"]],
                        "MonthlyIncome": [emp_row["MonthlyIncome"]],
                        "JobSatisfaction": [emp_row["JobSatisfaction"]],
                        "YearsAtCompany": [emp_row["YearsAtCompany"]],
                        "OverTime": [emp_row["OverTime"]]
                    })
                    emp_prob = model_pipeline.predict_proba(emp_input)[0][1] * 100

                    p_col1, p_col2, p_col3 = st.columns([1, 1, 1.2])
                    with p_col1:
                        st.markdown(f"**Employee:** `{emp_row['EmployeeID']}`")
                        st.markdown(f"**Department:** {emp_row['Department']}")
                        st.markdown(f"**Job Role:** {emp_row['JobRole']}")
                        st.markdown(f"**Age:** {emp_row['Age']} years")

                    with p_col2:
                        st.markdown(f"**Monthly Income:** ${emp_row['MonthlyIncome']:,}")
                        st.markdown(f"**Tenure:** {emp_row['YearsAtCompany']} years")
                        st.markdown(f"**OverTime:** {emp_row['OverTime']}")
                        st.markdown(f"**Job Satisfaction:** {emp_row['JobSatisfaction']} / 4")

                    with p_col3:
                        risk_color = "#10b981" if emp_prob < 30 else ("#f59e0b" if emp_prob < 60 else "#f43f5e")
                        risk_level = "Low Risk" if emp_prob < 30 else ("Moderate Risk" if emp_prob < 60 else "High Flight Risk")
                        st.markdown(f"""
                            <div style="background: rgba(99, 102, 241, 0.08); border-left: 4px solid {risk_color}; padding: 0.8rem 1rem; border-radius: 0 8px 8px 0;">
                                <div style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase;">ML Retention Assessment</div>
                                <div style="font-size: 1.4rem; font-weight: 800; color: {risk_color}; margin: 0.2rem 0;">{emp_prob:.1f}% Flight Probability</div>
                                <div style="font-size: 0.82rem; font-weight: 600;">Status: {risk_level} • Current Attrition: {emp_row['Attrition']}</div>
                            </div>
                        """, unsafe_allow_html=True)

        with st.expander("📊 View Descriptive Summary Statistics"):
            st.dataframe(display_df.describe().T, use_container_width=True)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
render_html("""
    <div style="text-align: center; color: #94a3b8; font-size: 0.78rem; margin-top: 2rem; padding: 1rem 0;">
        PulseHR Platform • Enterprise Workforce Intelligence & Predictive Talent Analytics
    </div>
""")
