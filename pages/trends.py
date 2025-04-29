import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_esg_zip

sns.set_style("whitegrid")
plt.rcParams["figure.facecolor"] = "white"

# -------------------------------------------------------------
# Load + sidebar filters
# -------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()

df = load_data()

years = sorted(df["year"].unique())
start, end = st.sidebar.slider(
    "Year range", int(years[0]), int(years[-1]), (int(years[0]), int(years[-1]))
)

divisions = sorted(df["Division"].dropna().unique())
sel_div = st.sidebar.selectbox("Division (heatmap)", ["All"] + divisions)

df_win = df[df["year"].between(start, end)]

# -------------------------------------------------------------
# Tabs: rolling-mean & YoY charts
# -------------------------------------------------------------
st.markdown("## 📈 ESG & Return Trends")

metrics_avail = ["ESG_Combined_Score", "ESG_Environmental_Score","ESG_Social_Score","ESG_Governance_Score","Total_Return"]
sel_metrics = st.multiselect("Metrics", metrics_avail, default=["ESG_Combined_Score","ESG_Environmental_Score","ESG_Social_Score","ESG_Governance_Score"])
window = st.slider("Rolling average window", 1, 5, 1, key="roll")

tab_line, tab_yoy = st.tabs(["Rolling Avg", "YoY % Change"])

# --- Rolling average line plot ---
with tab_line:
    if sel_metrics:
        fig, ax = plt.subplots(figsize=(8, 4))
        for m in sel_metrics:
            series = (
                df_win.groupby("year")[m]
                .mean()
                .rolling(window)
                .mean()
            )
            ax.plot(series.index, series.values, marker="o", label=m)
        ax.set_title(f"Rolling-{window}-Year Average ({start}–{end})")
        ax.set_xlabel("Year")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("Select at least one metric ⬆️")

# --- YoY bar plot ---
with tab_yoy:
    if "ESG_Combined_Score" in df.columns:
        esg_series = df_win.groupby("year")["ESG_Combined_Score"].mean()
        growth = esg_series.pct_change() * 100
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        bars = ax2.bar(
            growth.index,
            growth.values,
            color=["#2ca02c" if v > 0 else "#d62728" for v in growth.values],
        )
        ax2.axhline(0, color="gray", linewidth=0.8)
        ax2.set_title("YoY % Change – ESG Combined Score")
        ax2.set_ylabel("%")
        ax2.set_xlabel("Year")
        st.pyplot(fig2)

st.markdown("---")

# -------------------------------------------------------------
# Heatmap
# -------------------------------------------------------------
st.markdown("## 📊 ESG Heatmap by Division × Year")

heat_df = (
    df_win.groupby(["year", "Division"])["ESG_Combined_Score"]
    .mean()
    .unstack()
    .sort_index()
)

if sel_div != "All":
    heat_df = heat_df[[sel_div]]

fig3, ax3 = plt.subplots(figsize=(10, 0.5 * len(heat_df.columns) + 2))
sns.heatmap(
    heat_df.T if sel_div != "All" else heat_df,
    cmap="YlGnBu",
    linewidths=0.4,
    annot=False,
    cbar_kws={"label": "Avg ESG"},
    ax=ax3,
)
ax3.set_xlabel("Year")
ax3.set_ylabel("Division")
plt.xticks(rotation=90)
plt.yticks(rotation=0)
st.pyplot(fig3)
