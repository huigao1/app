import streamlit as st
st.set_page_config(page_title="ESG Analytics Suite", page_icon="💹", layout="wide")

# 页面注册

App_page_intro  = st.Page("pages/intro.py",              title="Welcome",              icon="🏠", default=True)
App_page_main   = st.Page("pages/main.py",               title="Dataset Overview",     icon="ℹ️")
App_page_eda    = st.Page("pages/eda.py",                title="Exploratory Analysis", icon="🔍")
App_page_ind    = st.Page("pages/industry.py",           title="Industry ESG",         icon="🏭")
App_page_trend  = st.Page("pages/trends.py",             title="Time-Series Trends",   icon="⏳")
App_page_reg    = st.Page("pages/linear_playground.py",  title="Regression Playground",icon="📈")
App_page_cluster= st.Page("pages/clustering.py",         title="Clustering (K-Means)", icon="🧩")
App_page_model  = st.Page("pages/model.py",              title="Model Training",       icon="🤖")
App_page_detail = st.Page("pages/details.py",            title="Model & Ratios", icon="📝")

pg = st.navigation({
    "Start":  [App_page_intro, App_page_main],
    "EDA":    [App_page_eda, App_page_ind, App_page_trend],
    "ML":     [App_page_reg, App_page_cluster, App_page_detail, App_page_model],
})

with st.sidebar:
    st.header("Navigation")
    st.markdown("Use the **top bar** to switch pages. Source: `esg_cleaned_final.csv.zip`")
pg.run()
