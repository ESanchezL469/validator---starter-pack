import json
import os
import shutil

import pytest
from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)

API_KEY = "supersecreta"
HEADERS = {"X-API-Key": API_KEY}

DATASETS_DIR = "datasets"
METADATA_DIR = "metadatas"
REPORTS_DIR = "reports"
PROFILES_DIR = "profiles"

TEST_HASH = "testhash123456"
FILENAME = f"{TEST_HASH}_data.csv"

# ---------- Setup (simula que ya has validado un dataset) ----------


@pytest.fixture(scope="module", autouse=True)
def setup_test_dataset():
    os.makedirs(DATASETS_DIR, exist_ok=True)
    os.makedirs(METADATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(PROFILES_DIR, exist_ok=True)

    # 1. CSV dataset
    with open(os.path.join(DATASETS_DIR, FILENAME), "w") as f:
        f.write("customerID,MonthlyCharges,Churn\n123,29.85,Yes")

    # 2. Metadata
    metadata = {
        "version": TEST_HASH,
        "timestamp": "20250709_142208",
        "columns": ["customerID", "MonthlyCharges", "Churn"],
        "total_rows": 1,
        "is_valid": True,
        "source_file": os.path.join(DATASETS_DIR, FILENAME),
        "replaces": "",
        "errors": [],
    }
    with open(os.path.join(METADATA_DIR, f"{TEST_HASH}_metadata.json"), "w") as f:
        json.dump(metadata, f)

    # 3. Report
    with open(os.path.join(REPORTS_DIR, f"{TEST_HASH}_report.txt"), "w") as f:
        f.write("Sample report.")

    # 4. Profile
    with open(os.path.join(PROFILES_DIR, f"{TEST_HASH}_profile.html"), "w") as f:
        f.write("<html><body>Sample profile</body></html>")

    yield  # 👈 Aquí se ejecutan los tests

    # Cleanup
    for path in [
        os.path.join(DATASETS_DIR, FILENAME),
        os.path.join(METADATA_DIR, f"{TEST_HASH}_metadata.json"),
        os.path.join(REPORTS_DIR, f"{TEST_HASH}_report.txt"),
        os.path.join(PROFILES_DIR, f"{TEST_HASH}_profile.html"),
    ]:
        if os.path.exists(path):
            os.remove(path)


# ---------- TESTS ----------


def test_get_dataset_metadata():
    response = client.get(f"/datasets/{TEST_HASH}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == TEST_HASH
    assert "columns" in data


def test_get_dataset_file():
    response = client.get(f"/datasets/file/{TEST_HASH}", headers=HEADERS)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "customerID" in response.content.decode()


def test_get_report_file():
    response = client.get(f"/reports/{TEST_HASH}", headers=HEADERS)
    assert response.status_code == 200
    assert "Sample report." in response.content.decode()


def test_get_dataset_history():
    response = client.get("/datasets/history", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(d.get("version") == TEST_HASH for d in data)


def test_get_profile_file():
    response = client.get(f"/profiles/{TEST_HASH}", headers=HEADERS)
    assert response.status_code == 200
    assert "<html>" in response.content.decode()


def test_get_nonexistent_metadata():
    response = client.get("/datasets/fakehash999", headers=HEADERS)
    assert response.status_code == 404
    assert response.json()["detail"] == "Metadata not found"
