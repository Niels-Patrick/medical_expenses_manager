import streamlit as st
import requests
import pandas as pd

st.title("Medical Expenses Manager")
st.write("User list")
    
def get_users():
    try:
        # Fetching all users from FastAPI
        response = requests.get("http://127.0.0.1:8000/users/users/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching user data: {e}")
        return []

users = get_users()

if users:
    df = pd.DataFrame(users)
    st.dataframe(df)
else:
    st.write("No user data available.")
