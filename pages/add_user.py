import streamlit as st
import requests
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import hashlib

# Loading .env file (only works locally)
load_dotenv()

# Retrieving the fernet key from the envrionment variable
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)
if not fernet:
    raise ValueError("FERNET_KEY environment variable is not set.")

def get_roles():
    """
    Fetches all roles from FastAPI

    Return:
        - the list of roles (or nothing if the request fails)
    """
    try:
        response = requests.get("http://127.0.0.1:8000/users/roles/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching role data: {e}")
        return []

# Getting data for user role
roles = get_roles()

# Getting only role names
role_data = [(role["id_role"], role["role_name"]) for role in roles]

role_names = [role[1] for role in role_data]

# Title and information
st.title("Medical Expenses Manager")
st.write("Add a new user")

# Creating a form to take user input
username = st.text_input("Username:")
password = st.text_input("Password:", type="password")
user_email = st.text_input("Email:")
user_role = st.selectbox("Role:", role_names)

if st.button("Submit"):
    id_role = next(role[0] for role in role_data if role[1] == user_role)

    # Sending the new user's data to FastAPI
    response = requests.post(
        "http://127.0.0.1:8000/users/add_user/",
        json={
            "username": username,
            "password": str(fernet.encrypt((hashlib.sha256(password.encode()).hexdigest()).encode())),
            "user_email": user_email,
            "user_role": str(id_role)
        }
    )

    if response.status_code == 200:
        result = response.json()
        st.write(f"{result['response_message']}")
        st.switch_page("pages/patient_list.py") # Rerouting to the patients list
    else:
        st.write(f"Error: {response.status_code}, {response.text}")