import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import load_esg_zip

@st.cache_data(show_spinner=False)
def load_data():
    return load_esg_zip()          # 默认读取根目录 zip

df = load_data()

import seaborn as sns

# Sidebar filters
years = sorted(df['year'].unique())
start, end = st.sidebar.slider("Year range", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))
divisions = sorted(df['Division'].dropna().unique())
sel_div = st.sidebar.selectbox("Division (heatmap)", ["All"] + divisions)

mask = df['year'].between(start, end)
df_win = df.loc[mask]

# ------------------------------------------------------------------
# Metric trend lines (multi‑select + rolling average)
# ------------------------------------------------------------------
metrics_avail = ['ESG_Combined_Score','Total_Return']
sel_metrics = st.multiselect("Select metrics to plot", metrics_avail, default=['ESG_Combined_Score'])
window = st.slider("Rolling average window (years)", 1, 5, 1)

if sel_metrics:
    fig, ax = plt.subplots(figsize=(8,4))
    for m in sel_metrics:
        series = df_win.groupby('year')[m].mean().rolling(window).mean()
        ax.plot(series.index, series.values, marker='o', label=m)
    ax.set_title(f"Rolling‑{window}-year Average \n({start}-{end})")
    ax.set_xlabel("Year"); ax.grid(True); ax.legend()
    st.pyplot(fig)

# ------------------------------------------------------------------
# YoY growth for ESG Combined
# ------------------------------------------------------------------
if 'ESG_Combined_Score' in df.columns:
    esg_series = df_win.groupby('year')['ESG_Combined_Score'].mean()
    growth = esg_series.pct_change()*100
    fig2, ax2 = plt.subplots(figsize=(8,3))
    ax2.bar(growth.index, growth.values, color=['green' if x>0 else 'red' for x in growth.values])
    ax2.set_title("Year‑over‑Year % Change – ESG Combined Score")
    ax2.set_ylabel('%'); ax2.axhline(0, color='black', linewidth=.8)
    st.pyplot(fig2)

# ------------------------------------------------------------------
# Heatmap: ESG by Division × Year
# ------------------------------------------------------------------
st.subheader("📊 ESG Heatmap by Division × Year")
heat_df = (df_win.groupby(['year','Division'])['ESG_Combined_Score'].mean()
                  .unstack().sort_index())
if sel_div != "All":
    heat_df = heat_df[[sel_div]]
fig3, ax3 = plt.subplots(figsize=(10,6))
sns.heatmap(heat_df.T if sel_div!='All' else heat_df, cmap='YlGnBu', ax=ax3, linewidths=.5)
ax3.set_xlabel('Year'); ax3.set_ylabel('Division')
st.pyplot(fig3)
