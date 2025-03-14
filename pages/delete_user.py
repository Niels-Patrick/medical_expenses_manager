import streamlit as st
import requests
    
# Initializing session state to track form visibility
if "edit_form_visible" not in st.session_state:
    st.session_state.edit_form_visible = False

# Title and information
st.title("Medical Expenses Manager")
st.write("Delete a user")

# Creating a form to take user ID input
id_user = st.number_input("Enter user ID to delete:", min_value=0, step=1)

if st.button("Delete User"):
    confirmation = st.empty()

    if id_user:
        st.session_state.edit_form_visible = True
        st.session_state.confirmation = confirmation

# Confirmation step after clicking on "Delete User"
if st.session_state.edit_form_visible:
    confirmation = st.session_state.confirmation

    with confirmation.container():
        st.warning("Are you sure you want to delete this user?")
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Yes, delete"):

                # Sending the id of the patient to delete to FastAPI
                response = requests.delete(f"http://127.0.0.1:8000/users/{id_user}/delete/")

                if response.status_code == 200:
                    result = response.json()
                    st.write(f"{result['response_message']}")
                    st.switch_page("pages/patient_list.py") # Rerouting to the patients list page
                else:
                    st.write(f"Error: {response.status_code}, {response.text}")
                
                confirmation.empty()

        with col2:
            if st.button("Cancel"):
                st.info("Deletion canceled.")
                confirmation.empty()
