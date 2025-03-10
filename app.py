import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/patients/"

st.title("Medical Expenses Manager")

# Fetching all patients from FastAPI
response = requests.get(API_URL)

if response.status_code == 200:
    patients = response.json()

    if patients:
        df = pd.DataFrame(patients)
        st.dataframe(df) # Alternatively: st.table(df)
    else:
        st.info("No patients available.")

else:
    st.error("Could not fetch patients.")
