import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_esg_zip

sns.set_style("whitegrid")

@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()

df = load_data()


st.markdown("<h2 style='margin-bottom:0.2em'>🧾 What Data Powers This Model?</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Year span", f"{df['year'].min()}–{df['year'].max()}")
c3.metric("Unique tickers", df['ticker_ann'].nunique())

st.divider()

st.markdown(
    """
This dataset is sourced from Wharton Research Data Services (WRDS) and includes both active and delisted U.S.-listed firms.
It merges structured financial statement data with annual, company-level ESG (Environmental, Social, and Governance) scores.

**Key Characteristics:**
- **Time Span:** 2002–2023 (earliest availability of ESG data)
- **Entities:** Publicly traded U.S. companies (active & inactive)
- **Coverage:** Firm fundamentals and annual ESG scores

The dataset enables longitudinal analysis of how financial performance and sustainability indicators evolve across industries and market cycles.
""",
    unsafe_allow_html=True,
)


plot_cols = ['ESG_Combined_Score','ESG_Environmental_Score','ESG_Social_Score','ESG_Governance_Score']
tabs = st.tabs([f"Dist • {c.split('_')[1]}" if c!='ESG_Combined_Score' else "Dist • Combined" for c in plot_cols])
for tab, col in zip(tabs, plot_cols):
    with tab:
        fig, ax = plt.subplots(figsize=(6,3))
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(col.replace('_',' '))
        st.pyplot(fig)

st.subheader("Yearly ESG vs Total Return Correlation")
corr = (
    df.dropna(subset=['ESG_Combined_Score','Total_Return'])
      .groupby('year')
      .apply(lambda g: g['ESG_Combined_Score'].corr(g['Total_Return']))
)
fig3, ax3 = plt.subplots(figsize=(8,3))
ax3.plot(corr.index, corr.values, marker='o', linewidth=2)
ax3.axhline(0, color='gray', linestyle='--')
ax3.set_xlabel('Year'); ax3.set_ylabel('Pearson r'); ax3.set_ylim(-1,1)
ax3.set_title('Correlation by Year')
st.pyplot(fig3)

st.caption("Hover over heatmap cells or use tabs for detailed distributions.")
