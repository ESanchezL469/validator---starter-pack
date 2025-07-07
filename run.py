from app.config import API_PORT
from app.setup import create_required_directories
import uvicorn

create_required_directories()

if __name__ == "__main__":
    uvicorn.run("app.api.main:app",host="0.0.0.0",port=API_PORT,reload=True)