import streamlit as st
import pandas as pd
from modules.frontend_methods import get_users
import logging

# Title and information
st.title("Medical Expenses Manager")
st.write("User list")

# Getting the list of all users
users = get_users()

# Displaying a dataframe of all users' data
if users:
    df = pd.DataFrame(users)
    st.dataframe(df)
else:
    logging.error("No user data available.")
    st.write("No user data available.")
