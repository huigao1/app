import streamlit as st
import pandas as pd
from utils import load_esg_zip

# -------------------------------------------------------------
# Hero / Landing
# -------------------------------------------------------------

st.title("🔍 <span style='color:red'>WHAT?</span> Forecasting Profitability with Financial & ESG Signals", unsafe_allow_html=True)

st.markdown("""
<span style='color:red'><strong>WHAT?</strong></span> — A dashboard that blends **financial ratios** with **ESG (Environmental, Social, Governance)** scores  
to predict two key profitability measures:

* **EBITDA Margin** – pre-financing operating profitability  
* **Operating Margin** – core efficiency after depreciation
""", unsafe_allow_html=True)

# ---------------- WHY ----------------
with st.expander("<span style='color:red'>WHY?</span> Importance", expanded=True):
    st.markdown("""
* <span style='color:red'>Investor Insight</span> – See how leverage, efficiency & ESG shifts move margins  
* <span style='color:red'>Strategic Planning</span> – Run *what-if* ESG scenarios and quantify impact  
* <span style='color:red'>Valuation Edge</span> – Dual-margin lens helps spot mispriced stocks
""", unsafe_allow_html=True)

# ---------------- HOW ----------------
with st.expander("<span style='color:red'>HOW?</span> Methodology", expanded=True):
    st.markdown("""
Predictions come from gradient-boosting & linear models trained on ~5 k firm-years, combining:

1. Market & accounting ratios (debt, turnover, ROA …)  
2. ESG pillar scores (environment, social, governance)  
3. Cross-validation to choose best hyper-parameters
""", unsafe_allow_html=True)

# ---------------- Why these targets ----------------
with st.expander("🎯 Why predict EBITDA & Operating Margins?"):
    st.markdown("""
| Metric | Reason for selection |
|--------|----------------------|
| **EBITDA Margin** | <ul><li>Strips out capital structure and non-cash items → comparable across firms</li><li>Highly correlated with enterprise-value multiples (EV/EBITDA)</li></ul> |
| **Operating Margin** | <ul><li>Captures full operating cost discipline (incl. D&A)</li><li>Key input in DCF valuations and a KPI tracked by management</li></ul> |
""", unsafe_allow_html=True)

# ---------------- ESG Pillars ----------------
with st.expander("🌿 ESG Pillars & Key Sub-Scores"):
    st.markdown("""
| Pillar | Sub-score | Dataset column | Captures |
|--------|-----------|----------------|----------|
| **Environmental** | Emissions | `ESG_Emissions_Score` | CO₂e footprint, reduction initiatives |
| | Environmental Overall | `ESG_Environmental_Score` | Resource use, waste, biodiversity |
| **Social** | Human Rights | `ESG_Human_Rights_Score` | Supplier labor standards |
| | Workforce | `ESG_Workforce_Score` | Diversity, safety, training |
| **Governance** | Governance Overall | `ESG_Governance_Score` | Board quality, exec pay, audit risk |
| – | Controversies | `ESG_Controversies_Score` | Litigation, scandals, fines |
""")

# ---------------- Next Steps ----------------
with st.expander("🚀 Next Steps", expanded=True):
    st.markdown("""
1. Use sidebar filters (year, division) on EDA pages  
2. Explore **Model Training** to see feature importance & tune parameters  
3. Try *Predict by Ticker* or *What-If Simulator* to stress ESG risk
""")

st.divider()

# -------------------------------------------------------------
# Dataset preview & download
# -------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return load_esg_zip()

df = load_data()

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())


st.markdown("---\n*Use the **navigation bar** at the top to explore EDA or modeling pages.*")
