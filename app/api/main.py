from fastapi import FastAPI

from app.api.routes import dataset, rules, validate
from app.init_dirs import create_required_directories

app = FastAPI(
    title="Starter Package API",
    description="Upload and process files with the Starter Package API",
    version="1.0.0",
)

create_required_directories()
app.include_router(validate.router)
app.include_router(dataset.router)
app.include_router(rules.router)
