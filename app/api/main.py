from fastapi import FastAPI
from app.init_dirs import create_required_directories
from app.api.routes.validate import router as validate_router

app = FastAPI(
    title="Starter Package API",
    description="Upload and process files with the Starter Package API",
    version="1.0.0"
)

create_required_directories()
app.include_router(validate_router, prefix="/validate", tags=["validate"])