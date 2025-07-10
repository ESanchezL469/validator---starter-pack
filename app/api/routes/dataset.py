import json
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.api.schemas.dataset import DatasetMetadata
from app.api.security import verify_api_key
from app.config import DATASETS_DIR, METADATA_DIR, PROFILES_DIR, REPORTS_DIR

router: APIRouter = APIRouter()


@router.get(
    "/datasets/history",
    summary="List all validated datasets",
    description="Returns a list of all validated datasets by reading their metadata files.",
    tags=["datasets"],
    dependencies=[Depends(verify_api_key)],
    response_model=list[DatasetMetadata],
    response_description="A list of metadata for each validated dataset",
)
def list_datasets() -> list[DatasetMetadata]:
    result: list[DatasetMetadata] = []

    for filename in os.listdir(METADATA_DIR):
        file_path = os.path.join(METADATA_DIR, filename)
        if filename.endswith("_metadata.json"):
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                try:
                    result.append(DatasetMetadata(**data))
                except Exception as e:
                    # Skip corrupted or invalid files
                    continue

    return result


@router.get(
    path="/datasets/{hash}",
    summary="Get metadata of a dataset version",
    description="Returns metadata such as columns, row count, errors and validation status for a given dataset version.",
    tags=["datasets"],
    responses={
        404: {"description": "Dataset not found"},
        401: {"description": "Unauthorized - Invalid API key"},
    },
    status_code=200,
    response_description="Dataset metadata returned successfully",
    dependencies=[Depends(verify_api_key)],
    response_model=DatasetMetadata,
)
def get_dataset_metadata(hash: str) -> dict:
    path: str = os.path.join(METADATA_DIR, f"{hash}_metadata.json")
    if not os.path.exists(path=path):
        raise HTTPException(status_code=404, detail="Metadata not found")
    with open(path) as f:
        return json.load(f)


@router.get(
    path="/datasets/file/{hash}",
    summary="Download validated dataset file",
    description="Returns the validated dataset (CSV) associated with the given hash.",
    tags=["datasets"],
    responses={
        200: {"description": "CSV file returned successfully"},
        404: {"description": "Dataset not found"},
        401: {"description": "Unauthorized - Invalid API key"},
    },
    response_description="A CSV file containing the dataset",
    dependencies=[Depends(verify_api_key)],
)
def get_dataset_file(hash: str) -> FileResponse:
    path: str = os.path.join(DATASETS_DIR, f"{hash}_data.csv")
    if not os.path.exists(path=path):
        raise HTTPException(status_code=404, detail="Dataset not found")
    return FileResponse(path, media_type="text/csv", filename=f"{hash}_data.csv")


@router.get(
    "/reports/{hash}",
    summary="Download validation report",
    description="Returns the text report generated after validating the dataset with the given hash.",
    tags=["reports"],
    responses={
        200: {"description": "Validation report returned successfully"},
        404: {"description": "Report not found"},
        401: {"description": "Unauthorized - Invalid API key"},
    },
    response_description="A text file containing the validation report",
    dependencies=[Depends(verify_api_key)],
)
def get_report_file(hash: str) -> FileResponse:
    path: str = os.path.join(REPORTS_DIR, f"{hash}_report.txt")
    if not os.path.exists(path=path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(path, media_type="text/csv", filename=f"{hash}_report.txt")


@router.get(
    "/profiles/{hash}",
    summary="Download profiling report",
    description="Returns the HTML profiling report generated for the dataset identified by the given hash.",
    tags=["profiling"],
    responses={
        200: {"description": "HTML profiling report returned successfully"},
        404: {"description": "Profiler report not found"},
        401: {"description": "Unauthorized - Invalid API key"},
    },
    response_description="An HTML file containing the profiling report",
    dependencies=[Depends(verify_api_key)],
)
def get_profiler_file(hash: str) -> FileResponse:
    path: str = os.path.join(PROFILES_DIR, f"{hash}_profile.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Profiler not found")
    return FileResponse(path, media_type="text/html", filename=f"{hash}_profile.html")
