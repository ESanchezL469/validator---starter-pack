import json
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from app.api.security import verify_api_key
from app.config import DATASETS_DIR, METADATA_DIR, PROFILES_DIR, REPORTS_DIR

router: APIRouter = APIRouter()


@router.get("/datasets/history", dependencies=[Depends(verify_api_key)])
def list_datasets() -> dict[str, list]:
    result: list[dict] = []
    for filename in os.listdir(METADATA_DIR):
        with open(os.path.join(METADATA_DIR, filename)) as f:
            metadata = json.load(f)
            result.append(metadata)
    return {"datasets": result}


@router.get(
    "/datasets/{hash}",
    summary="Get metadata of a versioned dataset",
    tags=["datasets"],
    responses={404: {"description": "Dataset not found"}},
    dependencies=[Depends(verify_api_key)],
)
def get_dataset_metadata(hash: str) -> dict:
    path: str = os.path.join(METADATA_DIR, f"{hash}_metadata.json")
    if not os.path.exists(path=path):
        raise HTTPException(status_code=404, detail="Metadata not found")
    with open(path) as f:
        return json.load(f)


@router.get("/datasets/file/{hash}", dependencies=[Depends(verify_api_key)])
def get_dataset_file(hash: str) -> FileResponse:
    path: str = os.path.join(DATASETS_DIR, f"{hash}_data.csv")
    if not os.path.exists(path=path):
        raise HTTPException(status_code=404, detail="Dataset not found")
    return FileResponse(path, media_type="text/csv", filename=f"{hash}_data.csv")


@router.get("/reports/{hash}", dependencies=[Depends(verify_api_key)])
def get_report_file(hash: str):
    path: str = os.path.join(REPORTS_DIR, f"{hash}_report.txt")
    if not os.path.exists(path=path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(path, media_type="text/csv", filename=f"{hash}_report.txt")


@router.get("/profiles/{hash}", dependencies=[Depends(verify_api_key)])
def get_profiler_file(hash: str):
    path: str = os.path.join(PROFILES_DIR, f"{hash}_profile.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Profiler not found")
    return FileResponse(path, media_type="text/html", filename=f"{hash}_profile.html")
