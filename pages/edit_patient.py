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

def get_regions():
    try:
        # Fetching all regions from FastAPI
        response = requests.get("http://127.0.0.1:8000/patients/regions/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching region data: {e}")
        return []

def get_smokers():
    try:
        # Fetching all smoker statuses from FastAPI
        response = requests.get("http://127.0.0.1:8000/patients/smokers/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching region data: {e}")
        return []
    
def get_sexes():
    try:
        # Fetching all sexes from FastAPI
        response = requests.get("http://127.0.0.1:8000/patients/sexes/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching region data: {e}")
        return []
    
def get_patient(id_patient):
    try:
        # Fetching a patient based on their ID
        response = requests.get(f"http://127.0.0.1:8000/patients/{id_patient}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching patient data: {e}")
        return None

# Getting data for region, smoker and sex
regions = get_regions()
smokers = get_smokers()
sexes = get_sexes()

# Getting only region names, smoker statues (yes/no) and sex labels
region_data = [(region["id_region"], region["region_name"]) for region in regions]
is_smoker_data = [(smoker["id_smoker"], smoker["is_smoker"]) for smoker in smokers]
sex_labels_data = [(sex["id_sex"], sex["sex_label"]) for sex in sexes]

region_names = [region[1] for region in region_data]
is_smoker = [smoker[1] for smoker in is_smoker_data]
sex_labels = [sex[1] for sex in sex_labels_data]

# Initializing session state to track form visibility
if "edit_form_visible" not in st.session_state:
    st.session_state.edit_form_visible = False

st.title("Medical Expenses Manager")
st.write("Edit a patient")


id_patient = st.number_input("Enter patient ID to edit:", min_value=0, step=1)

if st.button("Fetch patient"):
    patient = get_patient(id_patient)

    if patient:
        st.session_state.edit_form_visible = True
        st.session_state.patient = patient

if st.session_state.edit_form_visible:
    patient = st.session_state.patient

    # Creating a form to take patient input
    last_name = st.text_input("Last name:", value=patient["last_name"])
    first_name = st.text_input("First name:", value=patient["first_name"])
    age = st.text_input("Age:", value=patient["age"])
    bmi = st.text_input("BMI:", value=patient["bmi"])
    patient_email = st.text_input("Email:", value=patient["patient_email"])
    children = st.text_input("Number of children:", value=patient["children"])
    charges = st.text_input("Medical charges:", value=patient["charges"])
    region = st.selectbox("Region:", region_names, index=patient["region"])
    smoker = st.selectbox("Is smoker:", is_smoker, index=patient["smoker"])
    sex = st.selectbox("Sex:", sex_labels, index=patient["sex"])

    if st.button("Submit"):
        id_region = next(a_region[0] for a_region in region_data if a_region[1] == region)
        id_smoker = next(a_smoker[0] for a_smoker in is_smoker_data if a_smoker[1] == smoker)
        id_sex = next(a_sex[0] for a_sex in sex_labels_data if a_sex[1] == sex)

        response = requests.put(
            f"http://127.0.0.1:8000/patients/{id_patient}/edit/",
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
            st.switch_page("pages/patient_list.py")
        else:
            st.write(f"Error: {response.status_code}, {response.text}")
