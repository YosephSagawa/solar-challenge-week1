import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils import load_data

st.set_page_config(page_title="Solar Radiation Dashboard", layout="wide")

st.title("☀️ Cross-Country Solar Radiation Comparison")

# Load and preprocess
df = load_data()
df = df[(df['GHI'] > 20) & (df['DNI'] > 20) & (df['DHI'] > 20)]

# Sidebar widgets
countries = st.sidebar.multiselect(
    "Select Countries to Compare",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

metric = st.sidebar.selectbox("Select Metric", ["GHI", "DNI", "DHI"])

# Filtered data
df_filtered = df[df["Country"].isin(countries)]

# Boxplot
st.subheader(f"{metric} Distribution by Country")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df_filtered, x="Country", y=metric, ax=ax)
st.pyplot(fig)

# Summary Table
st.subheader("📊 Summary Statistics")
summary = df_filtered.groupby("Country")[metric].agg(["mean", "median", "std"]).reset_index()
st.dataframe(summary.round(2))

# Bar Chart
st.subheader("🏆 Average GHI by Country")
ghi_avg = df[df["Country"].isin(countries)].groupby("Country")["GHI"].mean().sort_values(ascending=False)
st.bar_chart(ghi_avg)
