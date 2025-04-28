import streamlit as st
st.set_page_config(page_title="ESG Analytics Suite", page_icon="💹", layout="wide")

# 页面注册

App_page_intro  = st.Page("pages/intro.py",              title="Welcome",              icon="🏠", default=True)
App_page_eda    = st.Page("pages/eda.py",                title="Exploratory Analysis", icon="🔍")
App_page_ind    = st.Page("pages/industry.py",           title="Industry ESG",         icon="🏭")
App_page_trend  = st.Page("pages/trends.py",             title="Time-Series Trends",   icon="⏳")
App_page_reg    = st.Page("pages/model_choice_playground.py",  title="Regression Playground",icon="📈")
App_page_cluster= st.Page("pages/clustering.py",         title="Clustering (K-Means)", icon="🧩")
App_page_detail = st.Page("pages/details.py",            title="Model & Ratios",       icon="📝")
App_page_predict = st.Page("pages/app.py",            title="Predict by Ticker",     icon="🎯")

pg = st.navigation({
    "Start":  [App_page_intro],
    "EDA":    [App_page_eda, App_page_ind, App_page_trend],
    "ML":     [App_page_cluster, App_page_detail, App_page_reg, App_page_predict],
})

with st.sidebar:
    st.header("Navigation")
    st.markdown("Use the **top bar** to switch pages. Source: `esg_cleaned_final.csv.zip`")
pg.run()
