import streamlit as st
import requests
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Loading .env file (only works locally)
load_dotenv()

# Retrieving the fernet key from the envrionment variable
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)
if not fernet:
    raise ValueError("FERNET_KEY environment variable is not set.")

def get_roles():
    try:
        # Fetching all roles from FastAPI
        response = requests.get("http://127.0.0.1:8000/users/roles/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching role data: {e}")
        return []
    
def get_user(id_user):
    try:
        # Fetching a user based on their ID
        response = requests.get(f"http://127.0.0.1:8000/users/{id_user}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching user data: {e}")
        return None

# Getting data for role
roles = get_roles()

# Getting only role names
role_data = [(role["id_role"], role["role_name"]) for role in roles]

role_names = [role[1] for role in role_data]

# Initializing session state to track form visibility
if "edit_form_visible" not in st.session_state:
    st.session_state.edit_form_visible = False

st.title("Medical Expenses Manager")
st.write("Edit a user")

id_user = st.number_input("Enter user ID to edit:", min_value=0, step=1)

if st.button("Fetch user"):
    user = get_user(id_user)

    if user:
        st.session_state.edit_form_visible = True
        st.session_state.user = user

if st.session_state.edit_form_visible:
    user = st.session_state.user

    # Creating a form to take user input
    username = st.text_input("Username:", value=user["username"])
    password = st.text_input("Password:", value=user["password"], type="password")
    user_email = st.text_input("Email:", value=user["user_email"])
    user_role = st.selectbox("Role:", role_names, index=user["user_role"])

    if st.button("Submit"):
        id_role = next(role[0] for role in role_data if role[1] == user_role)

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
            st.switch_page("pages/patient_list.py")
        else:
            st.write(f"Error: {response.status_code}, {response.text}")
