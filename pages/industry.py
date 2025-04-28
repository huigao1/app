import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import load_esg_zip

sns.set_style("whitegrid")

df = load_esg_zip()

st.markdown("<h2>🏭 Industry‑level ESG Overview</h2>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Average ESG by Division – full barh chart
# ------------------------------------------------------------------
ind = df.groupby('Division')['ESG_Combined_Score'].mean().sort_values()

st.subheader("Average ESG Combined Score by Division")
bar_height = max(4, min(len(ind)*0.3, 20))  # dynamic height
fig, ax = plt.subplots(figsize=(8, bar_height))
ind.plot(kind="barh", ax=ax, color="#1f77b4")
ax.set_xlabel("Average ESG Score (0‑100)")
ax.bar_label(ax.containers[0], fmt="{:.1f}", padding=3)
plt.tight_layout()
st.pyplot(fig)

# Top / Bottom tables
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🔝 Top 5 Divisions")
    st.dataframe(ind.tail(5).to_frame("Avg ESG").style.format("{:.2f}"))
with col2:
    st.markdown("#### 🔻 Bottom 5 Divisions")
    st.dataframe(ind.head(5).to_frame("Avg ESG").style.format("{:.2f}"))

st.divider()

# ------------------------------------------------------------------
# ESG trend over time (selectable divisions)
# ------------------------------------------------------------------
st.subheader("📈 ESG Combined Score Trend over Time")
all_divs = ind.index.tolist()
default_divs = ind.tail(5).index.tolist()  # default top‑5
sel_divs = st.multiselect("Choose divisions to plot", all_divs, default=default_divs)

if sel_divs:
    trend = (
        df[df['Division'].isin(sel_divs)]
        .groupby(['year','Division'])['ESG_Combined_Score']
        .mean()
        .unstack()
        .dropna(how='all')
    )
    fig2, ax2 = plt.subplots(figsize=(10,5))
    trend.plot(ax=ax2, marker='o')
    ax2.set_ylabel('Average ESG Score')
    ax2.set_xlabel('Year')
    ax2.set_ylim(0, 100)
    ax2.legend(title='Division', bbox_to_anchor=(1.02,1), loc='upper left')
    ax2.set_title('ESG Trend by Selected Divisions')
    plt.tight_layout()
    st.pyplot(fig2)
else:
    st.info("Select at least one division to display the time‑series plot.")
