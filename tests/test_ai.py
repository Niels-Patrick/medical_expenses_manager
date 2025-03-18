import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_charges_prediction():
    response = client.post("http://127.0.0.1:8000/AI/charges_prediction/", json={
        "age": "35",
        "sex": "female",
        "bmi": "18.2",
        "children": "0",
        "smoker": "no",
        "region": "southwest"
    })

    assert response.status_code == 200
