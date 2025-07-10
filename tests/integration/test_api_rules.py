import json
import os

from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)

API_KEY = "supersecreta"  # Usa una key válida en tu proyecto
HEADERS = {"X-API-Key": API_KEY}

RULES_DIR = "app/validation_rules"
TEST_FILENAME = "test_rules.json"

# Payload válido
VALID_PAYLOAD = {
    "filename": TEST_FILENAME,
    "rules": [
        {
            "column": "MonthlyCharges",
            "rule": "range",
            "description": "Between 0 and 500",
            "min": 0,
            "max": 500,
        },
        {"column": "Churn", "rule": "regex", "pattern": "^(Yes|No)$"},
    ],
}


def teardown_module(module):
    """Clean up test rules file"""
    path = os.path.join(RULES_DIR, TEST_FILENAME)
    if os.path.exists(path):
        os.remove(path)


def test_create_rule_file():
    response = client.post("/rules/", json=VALID_PAYLOAD, headers=HEADERS)
    assert response.status_code == 201
    assert "Rules saved as" in response.json()["message"]

    # Confirm file was saved
    path = os.path.join(RULES_DIR, TEST_FILENAME)
    assert os.path.exists(path)


def test_list_rule_files():
    response = client.get("/rules/", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert TEST_FILENAME in response.json()


def test_get_rule_file_contents():
    response = client.get(f"/rules/{TEST_FILENAME}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["column"] == "MonthlyCharges"


def test_get_nonexistent_rule_file():
    response = client.get("/rules/nonexistent.json", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Rules file not found"


def test_post_invalid_filename():
    payload = VALID_PAYLOAD.copy()
    payload["filename"] = "invalid_rules.txt"  # no termina en .json
    response = client.post("/rules/", json=payload, headers=HEADERS)
    assert response.status_code == 400
    assert response.json()["detail"] == "Filename must end with .json"
