# routers/rules.py

import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.schemas.rules import RuleFile
from app.api.security import verify_api_key
from app.config import RULES_DIR  # apuntando a app/validation_rules

router = APIRouter()


@router.post(
    "/rules/",
    summary="Create custom validation rules",
    description="Saves a custom rule set (as JSON) that can be later used in the dataset validation process.",
    tags=["rules"],
    response_description="Confirmation message with saved filename",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
def save_rules(rule_file: RuleFile) -> JSONResponse:
    filepath = os.path.join(RULES_DIR, rule_file.filename)

    if not rule_file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Filename must end with .json")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([rule.model_dump() for rule in rule_file.rules], f, indent=4)

        return JSONResponse(
            status_code=201, content={"message": f"Rules saved as {rule_file.filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not save rules")
