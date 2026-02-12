import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "backup-383605-20421239bd13.json", scope
)

client = gspread.authorize(creds)

sheet = client.open_by_key("SHEET_ID").sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)

st.dataframe(df.head())
