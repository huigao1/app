import streamlit as st

st.title("🏠 Welcome to the ESG Analytics Suite")

st.markdown("""
This interactive dashboard helps you **explore**, **analyze**, and **model** the relationship between
Environmental‑Social‑Governance (ESG) scores and key financial metrics.

### What you can do here
| Group | Page | Purpose |
|-------|------|---------|
| **Start** | **Dataset Overview** | Quick preview & download of the master dataset |
| **EDA** | Exploratory, Industry, Trends, Scatter Matrix | Visual deep‑dive with filters |
| **ML** | Regression Playground, K‑Means, Model Training | Build ad‑hoc regressions, cluster companies, benchmark ML models |
| **Docs** | About & Methodology | Data sources, formulas, and version info |

---
### Navigation tips
- Use the **navigation bar** at the top to switch pages.
- The **sidebar** on the left offers filters or help, depending on the page.
- Most tables are interactive: click column headers to sort or search.

Enjoy analyzing! If you have ideas for new features, open an issue in the repo.
""")
