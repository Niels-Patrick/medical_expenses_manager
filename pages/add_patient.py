import streamlit as st
import requests
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from modules.frontend_methods import get_regions, get_sexes, get_smokers
import logging

# Loading .env file (only works locally)
load_dotenv()

# Retrieving the fernet key from the envrionment variable
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)
if not fernet:
    logging.error("Error fetching FERNET_KEY")
    raise ValueError("FERNET_KEY environment variable is not set.")

# Getting data for region, smoker and sex
regions = get_regions()
smokers = get_smokers()
sexes = get_sexes()

# Getting only region names, smoker statues and sex labels
region_data = [(region["id_region"], region["region_name"]) for region in regions]
is_smoker_data = [(smoker["id_smoker"], smoker["is_smoker"]) for smoker in smokers]
sex_labels_data = [(sex["id_sex"], sex["sex_label"]) for sex in sexes]

region_names = [region[1] for region in region_data]
is_smoker = [smoker[1] for smoker in is_smoker_data]
sex_labels = [sex[1] for sex in sex_labels_data]

# Title and information
st.title("Medical Expenses Manager")
st.write("Add a new patient")

# Creating a form to take patient input
last_name = st.text_input("Last name:")
first_name = st.text_input("First name:")
age = st.text_input("Age:")
bmi = st.text_input("BMI:")
patient_email = st.text_input("Email:")
children = st.text_input("Number of children:")
charges = st.text_input("Medical charges:")
region = st.selectbox("Region:", region_names)
smoker = st.selectbox("Is smoker:", is_smoker)
sex = st.selectbox("Sex:", sex_labels)

if st.button("Submit"):
    id_region = next(a_region[0] for a_region in region_data if a_region[1] == region)
    id_smoker = next(a_smoker[0] for a_smoker in is_smoker_data if a_smoker[1] == smoker)
    id_sex = next(a_sex[0] for a_sex in sex_labels_data if a_sex[1] == sex)

    # Sending the new patient's data to FastAPI
    response = requests.post(
        "http://127.0.0.1:8000/patients/add_patient/",
        json={
            "last_name": str(fernet.encrypt(last_name.encode())),
            "first_name": str(fernet.encrypt(first_name.encode())),
            "age": age,
            "bmi": bmi,
            "patient_email": str(fernet.encrypt(patient_email.encode())),
            "children": children,
            "charges": charges,
            "region": str(id_region),
            "smoker": str(id_smoker),
            "sex": str(id_sex)
        }
    )

    if response.status_code == 200:
        result = response.json()
        st.write(f"{result['response_message']}")
        st.switch_page("pages/patient_list.py") # Rerouting to the patients list
    else:
        logging.error(f"Error {response.status_code}, {response.text}")
        st.write(f"Error: {response.status_code}, {response.text}")
