import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_esg_zip

st.markdown("<h2>🏭 Industry‑level ESG Dashboard</h2>", unsafe_allow_html=True)

df = load_esg_zip()

# -------------------------------------------------------------
# Bar — Average ESG by Division (interactive Plotly)
# -------------------------------------------------------------

div_avg = (
    df.groupby('Division')['ESG_Combined_Score']
      .mean()
      .round(2)
      .sort_values()
      .reset_index()
)

bar_fig = px.bar(
    div_avg,
    x='ESG_Combined_Score',
    y='Division',
    orientation='h',
    text='ESG_Combined_Score',
    color='ESG_Combined_Score',
    color_continuous_scale='Blues',
    labels={'ESG_Combined_Score':'Average ESG'},
    height=max(400, 25*len(div_avg)),
)
bar_fig.update_layout(coloraxis_showscale=False, margin=dict(l=120, r=10, t=30, b=30))
bar_fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

st.subheader("Average ESG Combined Score by Division")
st.plotly_chart(bar_fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🔝 Top 5 Divisions")
    st.table(div_avg.tail(5).iloc[::-1].set_index('Division'))
with col2:
    st.markdown("#### 🔻 Bottom 5 Divisions")
    st.table(div_avg.head(5).set_index('Division'))

# -------------------------------------------------------------
# Line — ESG Trend over Time for Selected Divisions
# -------------------------------------------------------------

st.markdown("---")
st.subheader("📈 ESG Trend Over Time")
all_divs   = div_avg['Division'].tolist()
default_sel = div_avg.tail(5)['Division'].tolist()
sel_divs = st.multiselect("Select divisions", all_divs, default=default_sel)

if sel_divs:
    trend = (
        df[df['Division'].isin(sel_divs)]
          .groupby(['year','Division'])['ESG_Combined_Score']
          .mean()
          .reset_index()
    )
    line_fig = px.line(
        trend,
        x='year', y='ESG_Combined_Score', color='Division',
        markers=True,
        labels={'ESG_Combined_Score':'Average ESG'},
        height=450,
    )
    line_fig.update_yaxes(range=[0,100])
    st.plotly_chart(line_fig, use_container_width=True)
else:
    st.info("Select at least one division to show trend lines.")
