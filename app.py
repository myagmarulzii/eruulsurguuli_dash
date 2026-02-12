import streamlit as st
import pandas as pd
import json
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

st.set_page_config(page_title="Эрүүл мэндийн Dashboard", layout="wide")

# Load credentials securely
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

credentials = Credentials.from_service_account_info(
    creds_dict,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)

client = gspread.authorize(credentials)

SHEET_ID = "s"
sheet = client.open_by_key(s).sheet1

@st.cache_data(ttl=300)
def load_data():
    return pd.DataFrame(sheet.get_all_records())

df = load_data()

st.title("📊 Сургуулийн Эрүүл Мэндийн Dashboard")

st.success("✅ Google Sheets холболт амжилттай")

# KPI
col1, col2 = st.columns(2)
col1.metric("Нийт мөр", len(df))
col2.metric("Багана", len(df.columns))

# Interactive Table
st.dataframe(df, use_container_width=True)

# Simple chart (if BMI column exists)
if "bmi" in df.columns:
    fig = px.histogram(df, x="bmi", title="BMI Distribution")
    st.plotly_chart(fig, use_container_width=True)
