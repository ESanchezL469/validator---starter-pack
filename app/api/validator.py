import os
import pandas as pd
from app.validators.schema import validate_dataframe
from app.enrichers.enricher import enrich_dataframe
from app.storage.storage import save_dataframe, calculate_hash
from app.storage.ingestor import load_file
from app.metadata.tracker import version_exists,find_previous_version
from app.metadata.metadata import save_metadata
from app.profilers.profiler import generate_profile
from app.reporters.reporter import generate_report

class DatasetValidator:

    def __init__(self,path:str = None, enableProfile:bool = False):
        self.path: str = path
        self.enableProfile: bool = enableProfile
        self.data: pd.DataFrame = None
        self.typeFile: str = None
        self.is_valid: bool = False
        self.error = {}
        self.version: str = None
        self.timestamp: str = None
        self.previous: str = None

    def run_pipeline(self)->str:

        if not os.path.exists(self.path):
            return f"File {self.path} does not exist."

        self.data, self.typeFile = load_file(self.path)
        self.is_valid, self.errors = validate_dataframe(self.data)
        self.data = enrich_dataframe(self.data)
        self.version = calculate_hash(self.data)

        if version_exists(self.version):
            return f'File {self.path} was already validate'
        
        self.version, self.timestamp = save_dataframe(self.data) #A corregir por referenca ciclica
        generate_profile(self.data,self.version) if self.enableProfile else 1
        generate_report(self.version, self.is_valid, self.errors, self.timestamp, self.data)
        self.previous = find_previous_version(self.version)
        save_metadata(self)

        return f'File {self.path} has validate'

