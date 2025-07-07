import os
from dotenv import load_dotenv

load_dotenv()

DATASETS_DIR = os.getenv("DATASETS_DIR", "datasets")
METADATA_DIR = os.getenv("METADATA_DIR", "metadatas")
REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")
PROFILES_DIR = os.getenv("PROFILES_DIR", "profiles")
API_PORT = int(os.getenv("API_PORT",8080))