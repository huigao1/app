import streamlit as st, matplotlib.pyplot as plt
from utils import load_esg_zip
df = load_esg_zip()

st.title("🏭 Industry ESG Overview")
ind = df.groupby('Division')['ESG_Combined_Score'].mean().sort_values()


c1, c2 = st.columns([2,1])
with c1:
    fig, ax = plt.subplots(figsize=(6,8))
    ind.plot(kind="barh", ax=ax)
    ax.set_xlabel("Average ESG")
    st.pyplot(fig)
with c2:
    st.write("#### 🔝 Top 5")
    st.dataframe(ind.tail(5).to_frame("ESG"))
    st.write("#### 🔻 Bottom 5")
    st.dataframe(ind.head(5).to_frame("ESG"))
