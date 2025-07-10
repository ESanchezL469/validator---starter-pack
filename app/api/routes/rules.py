# routers/rules.py

import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.schemas.rules import RuleFile, RuleSchema
from app.api.security import verify_api_key
from app.config import RULES_DIR

router = APIRouter()


@router.post(
    path="/rules/",
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


@router.get(
    "/rules/",
    summary="List available rule files",
    description="Returns the filenames of all saved rule sets available for validation.",
    tags=["rules"],
    response_description="A list of rule file names",
    dependencies=[Depends(verify_api_key)],
    response_model=list[str],
)
def list_rule_files() -> list[str]:
    try:
        files = [
            filename for filename in os.listdir(RULES_DIR) if filename.endswith(".json")
        ]
        return files
    except Exception:
        raise HTTPException(status_code=500, detail="Could not list rule files")


@router.get(
    "/rules/{filename}",
    summary="Get rule file contents",
    description="Returns the list of validation rules from the specified rule file.",
    tags=["rules"],
    response_description="A list of rule definitions",
    dependencies=[Depends(verify_api_key)],
    response_model=list[RuleSchema],
    responses={
        404: {"description": "Rules file not found"},
        400: {"description": "Invalid filename"},
    },
)
def get_rule_file(filename: str) -> list[RuleSchema]:
    if not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Filename must end with .json")

    filepath = os.path.join(RULES_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Rules file not found")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            rules_data = json.load(f)
        return [RuleSchema(**rule) for rule in rules_data]
    except Exception:
        raise HTTPException(status_code=500, detail="Could not read rules file")
