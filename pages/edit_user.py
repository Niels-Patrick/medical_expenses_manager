import streamlit as st
import requests
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from modules.frontend_methods import get_roles, get_user

# Loading .env file (only works locally)
load_dotenv()

# Retrieving the fernet key from the envrionment variable
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)
if not fernet:
    raise ValueError("FERNET_KEY environment variable is not set.")

# Getting data for role
roles = get_roles()

# Getting only role names
role_data = [(role["id_role"], role["role_name"]) for role in roles]

role_names = [role[1] for role in role_data]

# Initializing session state to track form visibility
if "edit_form_visible" not in st.session_state:
    st.session_state.edit_form_visible = False

# Title and information
st.title("Medical Expenses Manager")
st.write("Edit a user")

# Creating a form to take user ID input
id_user = st.number_input("Enter user ID to edit:", min_value=0, step=1)

if st.button("Fetch user"):
    user = get_user(id_user)

    if user:
        st.session_state.edit_form_visible = True
        st.session_state.user = user

# Creating a form to take user input
if st.session_state.edit_form_visible:
    user = st.session_state.user

    username = st.text_input("Username:", value=user["username"])
    password = st.text_input("Password:", value=user["password"], type="password")
    user_email = st.text_input("Email:", value=user["user_email"])
    user_role = st.selectbox("Role:", role_names, index=user["user_role"])

    if st.button("Submit"):
        id_role = next(role[0] for role in role_data if role[1] == user_role)

        # Sending the updated user's data to FastAPI
        response = requests.put(
            f"http://127.0.0.1:8000/users/{id_user}/edit/",
            json={
                "username": username,
                "password": str(fernet.encrypt(password.encode())),
                "user_email": user_email,
                "user_role": str(id_role)
            }
        )

        if response.status_code == 200:
            result = response.json()
            st.write(f"{result['response_message']}")
            st.switch_page("pages/patient_list.py") # Rerouting to the patients list page
        else:
            st.write(f"Error: {response.status_code}, {response.text}")
