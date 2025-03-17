import streamlit as st
import requests
from modules.frontend_methods import get_regions, get_sexes, get_smokers
import logging

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
st.write("Enter patient information to predict charges")

# Creating a form to take patient input
age = st.text_input("Age:")
bmi = st.text_input("BMI:")
children = st.text_input("Number of children:")
region = st.selectbox("Region:", region_names)
smoker = st.selectbox("Is smoker:", is_smoker)
sex = st.selectbox("Sex:", sex_labels)

if st.button("Submit"):

    # Sending the new patient's data to FastAPI
    response = requests.post(
        "http://127.0.0.1:8000/AI/charges_prediction/",
        json={
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region
        }
    )

    if response.status_code == 200:
        result = response.json()
        st.write(f"{result['response_message']}")
    else:
        logging.error(f"Error {response.status_code}, {response.text}")
        st.write(f"Error: {response.status_code}, {response.text}")
