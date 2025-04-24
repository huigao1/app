import streamlit as st

# -------------------------------------------------------------
# GLOBAL CONFIGURATION (must be first Streamlit call)
# -------------------------------------------------------------
st.set_page_config(page_title="ESG Analytics Dashboard", page_icon="💹", layout="wide")

# -------------------------------------------------------------
# PAGE REGISTRATION (file‑based)
# -------------------------------------------------------------
App_page_0 = st.Page("pages/main.py",     title="Dataset Overview",   icon="ℹ️", default=True)
App_page_1 = st.Page("pages/eda.py",      title="Exploratory Analysis", icon="🔍")
App_page_2 = st.Page("pages/industry.py", title="Industry ESG",        icon="🏭")
App_page_3 = st.Page("pages/trends.py",   title="Time‑Series Trends",  icon="⏳")
App_page_4 = st.Page("pages/model.py",    title="Model Training",      icon="🤖")

pg = st.navigation({
    "Start":  [App_page_0],
    "EDA":    [App_page_1, App_page_2, App_page_3],
    "Model":  [App_page_4],
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
