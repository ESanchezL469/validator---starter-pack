import os
import shutil
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse

from app.api.schemas.validate import ValidationResult
from app.api.security import verify_api_key
from app.api.validator import DatasetValidator
from app.core.logger import logger

router: APIRouter = APIRouter()


@router.post(
    "/validate/",
    summary="Validate uploaded dataset against rules",
    description="Validates an uploaded CSV or Excel dataset using a specified rules file and returns a validation summary.",
    tags=["validation"],
    status_code=200,
    response_model=ValidationResult,
    dependencies=[Depends(verify_api_key)],
    response_description="Result of validating the dataset against specified rules.",
)
def validate_file(
    file: UploadFile = File(...), rules_file: str = Query("customer.json")
) -> JSONResponse:
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path: str = tmp.name

        logger.info(f"File loaded: {file.filename}")
        logger.info(f"Using rules file: {rules_file}")

        rules_path: str = os.path.join("app/validation_rules", rules_file)

        validator: DatasetValidator = DatasetValidator(
            path=temp_path, enableProfile=True, rules_file=rules_path
        )
        result_msg: str = validator.run_pipeline()

        logger.info("Validation successful")

        return JSONResponse(
            {
                "status": (
                    "success"
                    if not validator.error and not validator.rules_error
                    else "error"
                ),
                "hash": validator.version,
                "filename": file.filename,
                "message": result_msg,
                "summary": {
                    "total_rows": (
                        validator.data.shape[0] if validator.data.empty else 0
                    ),
                    "total_columns": (
                        validator.data.shape[1] if validator.data.empty else 0
                    ),
                    "errors_found": (
                        0
                        if not validator.error
                        else sum(e["invalid_count"] for e in validator.error)
                    ),
                    "validation_passed": not validator.error,
                },
                "rules_error": validator.rules_error,
                "violations": validator.error,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {e}")
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass
