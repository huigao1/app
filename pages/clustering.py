import streamlit as st, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from utils import load_esg_zip

df = load_esg_zip()
vars = st.multiselect("Variables for clustering (numeric)", df.select_dtypes("number").columns, 
                      default=['ESG_Combined_Score','ROA','ROE','Debt_Ratio'])
k = st.slider("Number of clusters (k)", 2, 8, 3)

if len(vars) < 2:
    st.info("Pick at least 2 variables.")
    st.stop()

X = StandardScaler().fit_transform(df[vars].dropna())
km = KMeans(n_clusters=k, n_init='auto', random_state=0).fit(X)
df_plot = pd.DataFrame(X[:, :2], columns=['x','y'])
df_plot['cluster'] = km.labels_

st.title("🧩 K-Means Clustering")
fig, ax = plt.subplots()
sns.scatterplot(data=df_plot, x='x', y='y', hue='cluster', palette='tab10', ax=ax)
ax.set_xlabel(vars[0]); ax.set_ylabel(vars[1])
st.pyplot(fig)
