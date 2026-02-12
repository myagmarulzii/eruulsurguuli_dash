import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load data
df = pd.read_csv("student - s.csv")
df = df.dropna()

grades = ["1-р анги", "2-р анги", "3-р анги", "4-р анги", "5-р анги"]
df = df[df["academic_level_name"].isin(grades)]

# IQR filter
def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return data[(data[column] >= lower) & (data[column] <= upper)]

df = remove_outliers_iqr(df, "weight")
df = remove_outliers_iqr(df, "height")
df = remove_outliers_iqr(df, "bmi")

# BMI classification
def classify_bmi(bmi):
    if bmi < 14:
        return "Тураал"
    elif bmi <= 18.5:
        return "Хэвийн"
    else:
        return "Илүүдэл жин"

df["health_status"] = df["bmi"].apply(classify_bmi)

# Sidebar filter
selected_grade = st.sidebar.multiselect(
    "Анги сонгох",
    options=df["academic_level_name"].unique(),
    default=df["academic_level_name"].unique()
)

filtered_df = df[df["academic_level_name"].isin(selected_grade)]

# KPI
total = len(filtered_df)
under = (filtered_df["health_status"] == "Тураал").mean() * 100
normal = (filtered_df["health_status"] == "Хэвийн").mean() * 100
over = (filtered_df["health_status"] == "Илүүдэл жин").mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Нийт сурагч", total)
col2.metric("Тураал %", f"{under:.1f}%")
col3.metric("Хэвийн %", f"{normal:.1f}%")
col4.metric("Илүүдэл жин %", f"{over:.1f}%")

# Charts
fig1 = px.histogram(filtered_df, x="bmi", color="health_status", barmode="overlay")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    filtered_df.groupby(["academic_level_name", "health_status"]).size().reset_index(name="count"),
    x="academic_level_name",
    y="count",
    color="health_status",
    barmode="group"
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(filtered_df, x="height", y="weight", color="health_status")
st.plotly_chart(fig3, use_container_width=True)
