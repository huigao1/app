import streamlit as st
import plotly.express as px
from utils import load_esg_zip

st.markdown("## 🏭 Industry-level ESG Dashboard")

df = load_esg_zip()

# ───────────────────────────────────────────────────────────────
# Bar：Division 平均 ESG（渐变 & 数值标签）
# ───────────────────────────────────────────────────────────────
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

# ───────────────────────────────────────────────────────────────
# Line：多选 Division 的 ESG 走势
# ───────────────────────────────────────────────────────────────
all_divs = div_avg["Division"].tolist()
default_sel = div_avg.tail(5)["Division"].tolist()

sel_divs = st.multiselect("Select divisions to plot", all_divs, default=default_sel)
if sel_divs:
    trend = (
        df[df["Division"].isin(sel_divs)]
          .groupby(["year", "Division"])["ESG_Combined_Score"]
          .mean().reset_index()
    )
    line_fig = px.line(
        trend, x="year", y="ESG_Combined_Score", color="Division",
        markers=True, height=450,
        labels={"ESG_Combined_Score": "Average ESG"},
    )
    line_fig.update_yaxes(range=[0, 100])
    line_fig.update_layout(margin=dict(t=40, r=10, b=10))
    st.plotly_chart(line_fig, use_container_width=True)
else:
    st.info("⬅️ Pick at least one division to show its trend.")
