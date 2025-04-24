# Import Streamlit
import streamlit as st

# **** Page layout setup ****
App_page_0 = st.Page(
    "pages/main.py",
    title="Info about this App",
    default=True
)
App_page_1 = st.Page(
    "pages/page1.py",
    title="1) Model Training Code"
)
App_page_2 = st.Page(
    "pages/page2.py",
    title="2) Parameters of Trained Model"
)

# **** Set up navigation with section headers ****
pg = st.navigation(
    {
        "Start Here:": [App_page_0],
        "Dashboard Options": [App_page_1, App_page_2],
    }
)


# **** text/images shared on all pages ****
st.sidebar.markdown("Sidebar Prompts:")


# **** Execute the navigation code ****
pg.run()
