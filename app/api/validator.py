import os
import pandas as pd
import json

from app.core.logger import logger
from app.validators.schema import DataframeValidator
from app.validators.rule import validate_rule_structure
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
        self.error: list[dict] = None
        self.version: str = None
        self.timestamp: str = None
        self.previous: str = None,
        self.rules_error: list[dict] = None

    def load_rules(self, path: str = "validation_rules/customer.json") -> list[dict]:
        
        with open(path,"r") as f:
            data = json.load(f)
        
        if not isinstance(data,list) or not all(isinstance(item, dict) for item in data):
            logger.error(f"Invalid format in {path}: must be a list of dicts")
        
        return data

    def run_pipeline(self)->str:

        if not os.path.exists(self.path):
            logger.error(f"File {self.path} does not exist.")
            return f"File {self.path} does not exist."

        self.data, self.typeFile = load_file(self.path)
        
        validator: DataframeValidator = DataframeValidator(self.data)
        rules = self.load_rules()

        self.rules_error = validate_rule_structure(rules)

        if len(self.rules_error) > 0:
            logger.error('Error in rules')
            return f'Error in rules'

        self.error = validator.apply_rules(rules)
        self.is_valid = True if len(self.error) == 0 else False
        self.data = enrich_dataframe(self.data)
        self.version = calculate_hash(self.data)

        if version_exists(self.version):
            logger.info(f'File {self.path} was already validate')
            return f'File {self.path} was already validate'
        
        self.version, self.timestamp = save_dataframe(self.data) #A corregir por referenca ciclica
        generate_profile(self.data,self.version) if self.enableProfile else 1
        generate_report(self.version, self.is_valid, self.error, self.timestamp, self.data)
        self.previous = find_previous_version(self.version)
        save_metadata(self)

        logger.info(f'File {self.path} has been validated')
        return f'File {self.path} has been validated'