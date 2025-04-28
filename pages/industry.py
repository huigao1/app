import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_esg_zip

sns.set_theme(style="whitegrid")

df = load_esg_zip()

st.markdown("<h2 style='margin-bottom:0.2em'>🏭 Industry‑level ESG Overview</h2>", unsafe_allow_html=True)

# --------------------------------------------------
# Horizontal bar – average ESG per division
# --------------------------------------------------
avg_esg = df.groupby('Division')['ESG_Combined_Score'].mean().sort_values()

c_bar, c_tbl = st.columns([3,1])
with c_bar:
    fig, ax = plt.subplots(figsize=(7,6))
    sns.barplot(y=avg_esg.index, x=avg_esg.values, palette="viridis", ax=ax)
    ax.set_xlabel("Average ESG Score"); ax.set_ylabel("")
    ax.set_title("Mean ESG Combined by Division", loc="left")
    st.pyplot(fig)
with c_tbl:
    st.markdown("#### 🔝 Top 5")
    st.dataframe(avg_esg.tail(5).round(2).to_frame("ESG"))
    st.markdown("#### 🔻 Bottom 5")
    st.dataframe(avg_esg.head(5).round(2).to_frame("ESG"))

st.divider()

# --------------------------------------------------
# Time‑series trend per division
# --------------------------------------------------
st.markdown("### 📈 ESG Trends Across Years")

# optional filter – allow user to pick subset of divisions
all_divs = avg_esg.index.tolist()
sel_divs = st.multiselect("Select divisions to plot", all_divs, default=all_divs[:6])

trend = (df[df['Division'].isin(sel_divs)]
         .groupby(['year','Division'])['ESG_Combined_Score']
         .mean()
         .unstack())

fig2, ax2 = plt.subplots(figsize=(10,5))
trend.plot(ax=ax2, linewidth=2, marker='o')
ax2.set_ylabel("Avg ESG Score"); ax2.set_xlabel("Year")
ax2.set_title("ESG Combined Score Trends by Division")
ax2.legend(loc='upper left', bbox_to_anchor=(1.02,1))
ax2.grid(alpha=.3)
st.pyplot(fig2)

st.caption("Tip: deselect divisions to reduce clutter and focus on specific industries.")
