import os
import tempfile
import shutil
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.api.validator import DatasetValidator
from app.api.security import verify_api_key
from app.core.logger import logger

router = APIRouter()

@router.post("/",dependencies=[Depends(verify_api_key)])
def validate_file(file: UploadFile = File(...)):
    try:
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = tmp.name
        
        logger.info(f'File loaded: {file.filename}')

        validator = DatasetValidator(path=temp_path, enableProfile=True)
        result_msg = validator.run_pipeline()

        logger.info('Validation successful')

        return JSONResponse({
            "status": "success",
            "message": result_msg,
            "is_valid": validator.is_valid,
            "hash": validator.version,
            "total_rows": len(validator.data),
            "errors": validator.error,
            "report_url": f"/report/{validator.version}",
            "metadata_url": f"/metadatas/{validator.version}",
            "profile_url": f"/profile/{validator.version}" if validator.enableProfile else None
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass