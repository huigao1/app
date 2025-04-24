# Import Streamlit
import streamlit as st

# **** Page layout setup ****
App_page_0 = st.Page(
    "pages/main.py",
    title="Click here to select stock",
    default=True
)
App_page_1 = st.Page(
    "pages/page1.py",
    title="Page 1: See Raw Stock Data"
)
App_page_2 = st.Page(
    "pages/page2.py",
    title="Page 2: See Data Statistics"
)
App_page_3 = st.Page(
    "pages/page3.py",
    title="Page 3: See Stock Price Graph"
)

# **** Set up navigation with section headers ****
pg = st.navigation(
    {
        "Start Here:": [App_page_0],
        "Dashboard Options": [App_page_1, App_page_2, App_page_3],
    }
)


# **** text/images shared on all pages ****
st.sidebar.markdown("Sidebar Prompts:")


# **** Execute the navigation code ****
pg.run()
