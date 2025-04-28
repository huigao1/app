import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from utils import load_esg_zip

st.markdown("## 🏭 Industry-level ESG Dashboard")

df = load_esg_zip()

div_avg = (
    df.groupby("Division")["ESG_Combined_Score"]
      .mean().round(2).sort_values()
      .reset_index()
)

bar_fig = px.bar(
    div_avg, x="ESG_Combined_Score", y="Division",
    orientation="h", text="ESG_Combined_Score",
    color="ESG_Combined_Score", color_continuous_scale="Blues",
    labels={"ESG_Combined_Score": "Average ESG"},
    height=max(400, 25 * len(div_avg)),
)
bar_fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
bar_fig.update_layout(coloraxis_showscale=False, margin=dict(l=120, r=10, t=40, b=20))

st.plotly_chart(bar_fig, use_container_width=True)

col1, col2 = st.columns(2)
col1.write("#### 🔝 Top 5")
col1.table(div_avg.tail(5).iloc[::-1].set_index("Division"))
col2.write("#### 🔻 Bottom 5")
col2.table(div_avg.head(5).set_index("Division"))

st.markdown("---")

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
