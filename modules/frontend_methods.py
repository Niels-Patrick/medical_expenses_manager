import streamlit as st
import requests
import logging

def get_regions():
    """
    Fetches all regions from FastAPI

    Return:
        - the list of regions (or nothing if the request fails)
    """
    try:
        response = requests.get("http://127.0.0.1:8000/patients/regions/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching region data: {e}")
        st.error(f"Error fetching region data: {e}")
        return []

def get_smokers():
    """
    Fetches all smoker statuses from FastAPI

    Return:
        - the list of smoker statuses (or nothing if the request fails)
    """
    try:
        response = requests.get("http://127.0.0.1:8000/patients/smokers/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching smoker data: {e}")
        st.error(f"Error fetching smoker data: {e}")
        return []
    
def get_sexes():
    """
    Fetches all sexes from FastAPI

    Return:
        - the list of sexes (or nothing if the request fails)
    """
    try:
        response = requests.get("http://127.0.0.1:8000/patients/sexes/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching sex data: {e}")
        st.error(f"Error fetching sex data: {e}")
        return []
    
def get_patients():
    """
    Fetches all patients from FastAPI

    Return:
        - the list of patients (or nothing if the request fails)
    """
    try:
        response = requests.get("http://127.0.0.1:8000/patients/patients/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching patient data: {e}")
        st.error(f"Error fetching patient data: {e}")
        return []
    
def get_patient(id_patient):
    """
    Fetches a specific patient from FastAPI

    Parameters:
        - id_patient: the patient's ID

    Return:
        - the patient's data in JSON format (or None if the request fails)
    """
    try:
        response = requests.get(f"http://127.0.0.1:8000/patients/{id_patient}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching patient data: {e}")
        st.error(f"Error fetching patient data: {e}")
        return None
    
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
        logging.error(f"Error fetching role data: {e}")
        st.error(f"Error fetching role data: {e}")
        return []
    
def get_users():
    """
    Fetches all users from FastAPI

    Return:
        - the list of users (or nothing if the request fails)
    """
    try:
        # Fetching all users from FastAPI
        response = requests.get("http://127.0.0.1:8000/users/users/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching user data: {e}")
        st.error(f"Error fetching user data: {e}")
        return []
    
def get_user(id_user):
    """
    Fetches a specific user from FastAPI

    Parameters:
        - id_user: the user's ID

    Return:
        - the user's data in JSON format (or None if the request fails)
    """
    try:
        response = requests.get(f"http://127.0.0.1:8000/users/{id_user}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching user data: {e}")
        st.error(f"Error fetching user data: {e}")
        return None
