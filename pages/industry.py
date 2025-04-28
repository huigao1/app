import streamlit as st
import matplotlib.pyplot as plt
from utils import load_esg_zip

df = load_esg_zip()

st.title("🏭 Industry ESG Overview")

# ------------------------------------------------------------------
# Average ESG per Division (Bar + Top/Bottom tables)
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# ESG Trend by Division across Years (Line chart)
# ------------------------------------------------------------------
st.divider()
st.subheader("📈 ESG Combined Score Trends by Industry over Time")

trend = df.groupby(['year','Division'])['ESG_Combined_Score'].mean().unstack(fill_value=None)
fig2, ax2 = plt.subplots(figsize=(12,6))
trend.plot(ax=ax2)
ax2.set_title('ESG Combined Score Trends by Industry')
ax2.set_ylabel('ESG Score')
ax2.set_xlabel('Year')
ax2.legend(loc='upper left', bbox_to_anchor=(1.02,1))
st.pyplot(fig2)
