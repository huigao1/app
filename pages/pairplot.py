import streamlit as st, seaborn as sns
from utils import load_esg_zip
df = load_esg_zip()

cols = st.multiselect(
    "Select up to 5 numeric columns",
    df.select_dtypes("number").columns.tolist(),
    default=['ESG_Combined_Score','ROA','ROE']
)[:5]

if len(cols) >= 2:
    st.title("🔀 Scatter Matrix (pairplot)")
    g = sns.pairplot(df[cols].dropna(), diag_kind="kde", corner=True)
    st.pyplot(g.fig)
else:
    st.info("Pick at least 2 columns.")
