import streamlit as st
import pandas as pd
import json
import gspread
from google.oauth2.service_account import Credentials

creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

credentials = Credentials.from_service_account_info(
    creds_dict,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)

client = gspread.authorize(credentials)

sheet = client.open_by_key("s").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.dataframe(df.head())
