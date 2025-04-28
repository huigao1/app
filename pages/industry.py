import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_esg_zip

# A clean seaborn style for all plots
sns.set_theme(style="whitegrid")

df = load_esg_zip()

st.markdown("<h2 style='margin-bottom:0.5em'>🏭 Industry‑level ESG Overview</h2>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Average ESG per Division (vertical bar with angled labels)
# ------------------------------------------------------------------
ind = df.groupby('Division')['ESG_Combined_Score'].mean().sort_values(ascending=False)

c1, c2 = st.columns([4, 1])
with c1:
    fig, ax = plt.subplots(figsize=(10, 5))
    ind.plot(kind="bar", ax=ax, color=sns.color_palette("Blues_r", len(ind)))
    ax.set_ylabel("Average ESG Combined Score")
    ax.set_xlabel("")
    ax.set_title("Average ESG by Industry")
    plt.xticks(rotation=45, ha="right")  # tilt labels to avoid overlap
    sns.despine()
    st.pyplot(fig)

with c2:
    st.write("#### 🔝 Top 5")
    st.dataframe(ind.head(5).to_frame("Avg ESG"))
    st.write("#### 🔻 Bottom 5")
    st.dataframe(ind.tail(5).sort_values().to_frame("Avg ESG"))

# ------------------------------------------------------------------
ind = df.groupby('Division')['ESG_Combined_Score'].mean().sort_values()

c1, c2 = st.columns([3, 1])
with c1:
    fig, ax = plt.subplots(figsize=(7, 8))
    ind.plot(kind="barh", ax=ax)
    ax.set_xlabel("Average ESG Combined Score")
    ax.set_title("Average ESG by Industry (lower → higher)")
    ax.invert_yaxis()  # highest value at top
    st.pyplot(fig)

with c2:
    st.write("#### 🔝 Top 5 Industries (ESG)")
    st.dataframe(ind.tail(5).sort_values(ascending=False).to_frame("Avg ESG"))
    st.write("#### 🔻 Bottom 5")
    st.dataframe(ind.head(5).to_frame("Avg ESG"))

# ------------------------------------------------------------------
# ESG trend lines by Division
# ------------------------------------------------------------------
st.divider()
st.subheader("📈 ESG Combined Score Trends by Industry")

trend = (
    df.groupby(['year', 'Division'])['ESG_Combined_Score']
      .mean()
      .unstack()
      .sort_index()
)

fig2, ax2 = plt.subplots(figsize=(12, 6))
trend.plot(ax=ax2, linewidth=2)
ax2.set_ylabel('Average ESG Score'); ax2.set_xlabel('Year')
ax2.set_title('ESG Evolution by Division')
ax2.grid(alpha=0.3)
ax2.legend(title='Division', bbox_to_anchor=(1.02, 1), loc='upper left', ncol=1, frameon=False)
st.pyplot(fig2)

st.caption("Use legend to toggle industries; higher lines indicate better ESG performance over time.")
