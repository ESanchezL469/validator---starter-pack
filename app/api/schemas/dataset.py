from typing import List, Optional, Union

from pydantic import BaseModel


class ValidationError(BaseModel):
    column: str
    rule: str
    description: str
    invalid_count: int
    sample_invalid_values: List[Optional[Union[str, float, int, None]]]


class DatasetMetadata(BaseModel):
    version: str
    timestamp: str  # Ej: "20250709_142208"
    columns: List[str]
    total_rows: int
    is_valid: bool
    source_file: str
    replaces: Optional[str] = ""  # cadena vacía si no reemplaza
    errors: List[ValidationError]

    class Config:  # 👈 debe estar dentro del modelo
        schema_extra = {
            "example": {
                "version": "df7f38961a3e96888fce04e34cdd7bd19e5bd5c93830f108aca102e065a9365b",
                "timestamp": "20250709_142208",
                "columns": ["customerID", "MonthlyCharges", "PaymentMethod"],
                "total_rows": 50,
                "is_valid": False,
                "source_file": "/tmp/sample.csv",
                "replaces": "",
                "errors": [
                    {
                        "column": "MonthlyCharges",
                        "rule": "range",
                        "description": "Out of range (0-500)",
                        "invalid_count": 1,
                        "sample_invalid_values": [-50.0],
                    }
                ],
            }
        }
