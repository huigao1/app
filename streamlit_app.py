import streamlit as st

st.set_page_config(page_title="ESG Analytics Suite", page_icon="💹", layout="wide")

# 页面注册
App_page_0 = st.Page("pages/main.py",     title="Dataset Overview",  icon="ℹ️", default=True)
App_page_1 = st.Page("pages/eda.py",      title="Exploratory Analysis", icon="🔍")
App_page_2 = st.Page("pages/industry.py", title="Industry ESG",      icon="🏭")
App_page_3 = st.Page("pages/trends.py",   title="Time-Series Trends", icon="⏳")
App_page_4 = st.Page("pages/pairplot.py", title="Scatter Matrix",    icon="🔀")
App_page_5 = st.Page("pages/linear_playground.py", title="Regression Playground", icon="📈")
App_page_6 = st.Page("pages/clustering.py", title="Clustering (K-Means)", icon="🧩")
App_page_7 = st.Page("pages/model.py",    title="Model Training",    icon="🤖")
App_page_8 = st.Page("pages/about.py",    title="About & Docs",     icon="📄")

pg = st.navigation({
    "Start":  [App_page_0],
    "EDA":    [App_page_1, App_page_2, App_page_3, App_page_4],
    "ML":     [App_page_5, App_page_6, App_page_7],
    "Docs":   [App_page_8],
})

# -------------------------------------------------------------
# SIDEBAR (shared across all pages)
# -------------------------------------------------------------
with st.sidebar:
    st.header("About this app")
    st.markdown(
        "Explore **ESG metrics** and their relationship to earnings manipulation.\n\n"
        "Use the **navigation bar** above to switch pages."
    )

# -------------------------------------------------------------
# RUN SELECTED PAGE
# -------------------------------------------------------------
pg.run()
