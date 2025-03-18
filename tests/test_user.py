import pytest
from fastapi.testclient import TestClient
from main import app
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import logging
import os
import hashlib

client = TestClient(app)

# Loading .env file (only works locally)
load_dotenv()

# Retrieving the fernet key from the envrionment variable
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)
if not fernet:
    logging.error("Error fetching FERNET_KEY")
    raise ValueError("FERNET_KEY environment variable is not set.")

def test_get_all_app_users():
    response = client.get("http://127.0.0.1:8000/users/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_authentication():
    response = client.post("http://127.0.0.1:8000/users/auth/", json={
        "username": "JohnShepard2",
        "password": "Gsd234@"
    })

    assert response.status_code == 200
    assert response.json()["response_message"] == "User authenticated."

def test_add_user():
    response = client.post("http://127.0.0.1:8000/users/add_user/", json={
        "username": "JohnDoe",
        "password": str(fernet.encrypt((hashlib.sha256("test".encode()).hexdigest()).encode())),
        "user_email": "john.doe@gmail.com",
        "user_role": "2"
    })

    assert response.status_code == 200
    assert response.json()["response_message"] == "New user added."

def test_get_a_user():
    response = client.get("http://127.0.0.1:8000/users/13/")

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["username"] == "JohnDoe"

def test_edit_user():
    response = client.put("http://127.0.0.1:8000/users/13/edit/", json={
        "username": "JaneDoe",
        "password": str(fernet.encrypt((hashlib.sha256("test".encode()).hexdigest()).encode())),
        "user_email": "jane.doe@gmail.com",
        "user_role": "2"
    })

    assert response.status_code == 200
    assert response.json()["response_message"] == "User updated successfully."

def test_delete_a_patient():
    response = client.delete("http://127.0.0.1:8000/users/13/delete/")

    assert response.status_code == 200
    assert response.json()["response_message"] == "User deleted successfully."
