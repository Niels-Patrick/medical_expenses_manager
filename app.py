import streamlit as st
import requests

st.title("Medical Expenses Manager")
st.write("Log in")

# Creating a form to take user input
username_input = st.text_input("Username:")
password_input = st.text_input("Password:", type="password")

if st.button("Submit"):
    if username_input and password_input:
        response = requests.post(
            "http://127.0.0.1:8000/users/auth/",
            json={
                "username": username_input,
                "password": password_input
            }
        )

        if response.status_code == 200:
            result = response.json()
            st.write(f"{result['response_message']}")
            if result['response_message'] == "User authenticated.":
                st.switch_page("pages/patient_list.py")
        else:
            st.write(f"Error: {response.status_code}, {response.text}")
