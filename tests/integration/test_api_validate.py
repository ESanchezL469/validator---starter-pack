import io

import pandas as pd
from fastapi.testclient import TestClient

from app.api.main import \
    app  # Asegúrate de importar tu FastAPI app correctamente

client = TestClient(app)

VALID_API_KEY = "supersecreta"  # De prueba


# 📄 CSV válido simulado como archivo
def generate_valid_csv():
    content = (
        "id,name,email,age,created_at,is_active\n"
        "1,Ana,a@a.com,25,2024-01-01,True\n"
        "2,Luis,b@b.com,30,2024-02-01,True"
    )
    return io.BytesIO(content.encode("utf-8"))


# 📄 CSV con errores (age fuera de rango)
def generate_invalid_csv():
    content = "id,email,age,name\n1,a@a.com,10,Ana\n2,b@b.com,200,Luis"
    return io.BytesIO(content.encode("utf-8"))


# 🧪 Test de validación exitosa
def test_validate_valid_csv(monkeypatch):

    monkeypatch.setattr(
        "app.api.routes.validate.DatasetValidator.run_pipeline",
        lambda self: (
            setattr(
                self,
                "data",
                pd.DataFrame(
                    {
                        "id": [1, 2],
                        "name": ["Ana", "Luis"],
                        "email": ["a@a.com", "b@b.com"],
                        "age": [25, 30],
                        "created_at": ["2024-01-01", "2024-02-01"],
                        "is_active": [True, True],
                    }
                ),
            ),
            setattr(self, "error", []),
            setattr(self, "rules_error", []),
            "File sample.csv has been validated",
        ),
    )

    files = {"file": ("sample.csv", generate_valid_csv(), "text/csv")}
    headers = {"x-api-key": VALID_API_KEY}
    response = client.post(
        "http://0.0.0.0:8080/validate/", files=files, headers=headers
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["filename"] == "sample.csv"
    assert payload["summary"]["validation_passed"] is True


# 🧪 Test de validación con errores
def test_validate_invalid_csv(monkeypatch):

    monkeypatch.setattr(
        "app.api.routes.validate.DatasetValidator.run_pipeline",
        lambda self: (
            setattr(
                self,
                "data",
                pd.DataFrame(
                    {
                        "id": [1, 2],
                        "name": ["Ana", "Luis"],
                        "email": ["a@a.com", "b@b.com"],
                        "age": [10, 200],
                        "created_at": ["2024-01-01", "2024-02-01"],
                        "is_active": [True, False],
                    }
                ),
            ),
            setattr(
                self,
                "error",
                [
                    {
                        "column": "age",
                        "rule": "range",
                        "invalid_count": 2,
                        "sample_invalid_values": [10, 200],
                    }
                ],
            ),
            setattr(self, "rules_error", []),
            "File sample.csv has been validated with errors",
        )[-1],
    )

    files = {"file": ("sample.csv", generate_invalid_csv(), "text/csv")}
    headers = {"x-api-key": VALID_API_KEY}
    response = client.post("/validate/", files=files, headers=headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["summary"]["errors_found"] == 2
    assert payload["summary"]["validation_passed"] is False


# 🧪 Test sin archivo
def test_validate_missing_file():
    headers = {"x-api-key": VALID_API_KEY}
    response = client.post("http://0.0.0.0:8080/validate/", headers=headers)
    assert response.status_code == 422


# 🧪 Test sin API key
def test_validate_without_api_key():
    files = {"file": ("sample.csv", generate_valid_csv(), "text/csv")}
    response = client.post("http://0.0.0.0:8080/validate/", files=files)
    assert response.status_code == 422
