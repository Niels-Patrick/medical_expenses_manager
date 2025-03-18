import pytest
from fastapi.testclient import TestClient
from main import app
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import logging
import os

client = TestClient(app)

# Loading .env file (only works locally)
load_dotenv()

# Retrieving the fernet key from the envrionment variable
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)
if not fernet:
    logging.error("Error fetching FERNET_KEY")
    raise ValueError("FERNET_KEY environment variable is not set.")

def test_get_patients():
    response = client.get("http://127.0.0.1:8000/patients/patients/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_regions():
    response = client.get("http://127.0.0.1:8000/patients/regions/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_smokers():
    response = client.get("http://127.0.0.1:8000/patients/smokers/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_sexes():
    response = client.get("http://127.0.0.1:8000/patients/sexes/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_patient():
    response = client.post("http://127.0.0.1:8000/patients/add_patient/", json={
        "last_name": str(fernet.encrypt("Doe".encode())),
        "first_name": str(fernet.encrypt("John".encode())),
        "age": "24",
        "bmi": "18.1",
        "patient_email": str(fernet.encrypt("john.doe@gmail.com".encode())),
        "children": "1",
        "charges": "3000.00",
        "region": "1",
        "smoker": "0",
        "sex": "1"
    })

    assert response.status_code == 200
    assert response.json()["response_message"] == "New patient added."

def test_get_patient():
    response = client.get("http://127.0.0.1:8000/patients/1346/")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["last_name"] == "Doe"

def test_edit_patient():
    response = client.put("http://127.0.0.1:8000/patients/1346/edit/", json={
        "last_name": str(fernet.encrypt("Doe".encode())),
        "first_name": str(fernet.encrypt("Jane".encode())),
        "age": "24",
        "bmi": "18.1",
        "patient_email": str(fernet.encrypt("jane.doe@gmail.com".encode())),
        "children": "1",
        "charges": "3000.00",
        "region": "1",
        "smoker": "0",
        "sex": "0"
    })

    assert response.status_code == 200
    assert response.json()["response_message"] == "Patient updated successfully."

def test_delete_a_patient():
    response = client.delete("http://127.0.0.1:8000/patients/1346/delete/")

    assert response.status_code == 200
    assert response.json()["response_message"] == "Patient deleted successfully."
