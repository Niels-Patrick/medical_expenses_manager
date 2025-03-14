import streamlit as st
import requests
import pandas as pd
from modules.frontend_methods import get_patients

# Title and information
st.title("Medical Expenses Manager")
st.write("Patient list")

# Getting the list of all patients
patients = get_patients()

# Displaying a dataframe of all patients' data
if patients:
    df = pd.DataFrame(patients)
    st.dataframe(df)
else:
    st.write("No patient data available.")
