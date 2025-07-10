# schemas/rules.py
from typing import List, Optional

from pydantic import BaseModel, Field


class RuleSchema(BaseModel):
    column: str
    rule: str
    description: Optional[str] = ""
    min: Optional[float] = None
    max: Optional[float] = None
    pattern: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "column": "MonthlyCharges",
                "rule": "range",
                "description": "Charges must be between 0 and 500",
                "min": 0,
                "max": 500,
            }
        }


class RuleFile(BaseModel):
    filename: str = Field(..., example="custom_rules.json")
    rules: List[RuleSchema]
