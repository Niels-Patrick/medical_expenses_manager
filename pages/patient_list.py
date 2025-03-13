import streamlit as st
import requests
import pandas as pd

st.title("Medical Expenses Manager")
st.write("Patient list")
    
def get_patients():
    try:
        # Fetching all patients from FastAPI
        response = requests.get("http://127.0.0.1:8000/patients/patients/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching patient data: {e}")
        return []

patients = get_patients()

if patients:
    df = pd.DataFrame(patients)
    st.dataframe(df)
else:
    st.write("No patient data available.")