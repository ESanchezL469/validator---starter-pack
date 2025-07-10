from typing import List, Optional, Union

from pydantic import BaseModel


class ValidationError(BaseModel):
    column: str
    rule: str
    description: str
    invalid_count: int
    sample_invalid_values: List[Optional[Union[str, float, int, None]]]


class ValidationSummary(BaseModel):
    total_rows: int
    total_columns: int
    errors_found: int
    validation_passed: bool


class ValidationResult(BaseModel):
    status: str  # "success" o "error"
    hash: str
    filename: str
    message: str
    summary: ValidationSummary
    rules_error: bool
    violations: List[ValidationError]

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "hash": "df7f3896...",
                "filename": "data.csv",
                "message": "Validation completed successfully.",
                "summary": {
                    "total_rows": 50,
                    "total_columns": 10,
                    "errors_found": 0,
                    "validation_passed": True,
                },
                "rules_error": False,
                "violations": [],
            }
        }
