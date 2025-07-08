import json
import os
from typing import Any

import pandas as pd

from app.core.logger import logger
from app.enrichers.enricher import enrich_dataframe
from app.metadata.metadata import save_metadata
from app.metadata.tracker import find_previous_version, version_exists
from app.profilers.profiler import generate_profile
from app.reporters.reporter import generate_report
from app.storage.ingestor import load_file
from app.storage.storage import calculate_hash, save_dataframe
from app.validators.rule import validate_rule_structure
from app.validators.schema import DataframeValidator


class DatasetValidator:
    """
    Main pipeline class for validating, enriching, and storing a dataset.

    Attributes:
        path (str): Path to the uploaded file.
        enableProfile (bool): Whether to generate a profiling report.
        data (pd.DataFrame): Loaded dataset.
        typeFile (str): Type of the uploaded file.
        is_valid (bool): Whether the dataset passed validation.
        error (list[dict]): List of rule violations.
        version (str): Hash-based version of the dataset.
        timestamp (str): Timestamp when dataset was saved.
        previous (str): Previous version hash.
        rules (list[dict]): Rules of validation.
        rules_error (list[str]): Errors found.
    """

    def __init__(self, path: str = "", enableProfile: bool = False) -> None:
        """
        Initialize the DatasetValidator.

        Args:
            path (str): Path to the dataset file.
            enableProfile (bool): Whether to generate profiling output.
        """
        self.path: str = path
        self.enableProfile: bool = enableProfile
        self.data: pd.DataFrame = None
        self.typeFile: str = ""
        self.is_valid: bool = False
        self.error: list[dict] = []
        self.version: str = ""
        self.timestamp: str = ""
        self.previous: str = ""
        self.rules: list[dict] = []
        self.rules_error: list[str] = []

    def load_rules(self, path: str = "validation_rules/customer.json") -> Any:
        """
        Load validation rules from a JSON file.

        Args:
            path (str): Path to the JSON file.

        Returns:
            list[dict]: Loaded validation rules.
        """

        with open(path, "r") as f:
            data = json.load(f)

        if not isinstance(data, list) or not all(
            isinstance(item, dict) for item in data
        ):
            logger.error(f"Invalid format in {path}: must be a list of dicts")

        return data

    def run_pipeline(self) -> str:
        """
        Execute the full validation pipeline.

        Returns:
            str: Message indicating the result of validation.
        """

        if not self._file_exists():
            logger.error(f"File {self.path} does not exist.")
            return f"File {self.path} does not exist."

        self._load_data()
        self._load_and_validate_rules()

        if self.rules_error:
            logger.error("Error in rules")
            return "Error in rules"

        self._validate_data()
        self._enrich_data()
        self._calculate_version()

        if version_exists(self.version):
            logger.info(f"File {self.path} was already validate")
            return f"File {self.path} was already validate"

        self._store_dataset()
        self._generate_outputs()
        self._save_metadata()

        logger.info(f"File {self.path} has been validated")
        return f"File {self.path} has been validated"

    def _file_exists(self) -> bool:
        """Check if the dataset file exists."""
        return os.path.exists(self.path)

    def _load_data(self) -> None:
        """Load dataset file and determine file type."""
        self.data, self.typeFile = load_file(self.path)

    def _load_and_validate_rules(self) -> None:
        """Load rules and check for rule structure errors."""
        rules = self.load_rules()
        self.rules_error = validate_rule_structure(rules)
        self.rules = rules

    def _validate_data(self) -> None:
        """Apply validation rules to the dataset."""
        validator = DataframeValidator(self.data)
        self.error = validator.apply_rules(self.rules)
        self.is_valid = len(self.error) == 0

    def _enrich_data(self) -> None:
        """Enrich dataset with additional transformations."""
        self.data = enrich_dataframe(self.data)

    def _calculate_version(self) -> None:
        """Generate hash version for the dataset."""
        self.version = calculate_hash(self.data)

    def _store_dataset(self) -> None:
        """Persist validated dataset to disk."""
        self.version, self.timestamp = save_dataframe(self.data)

    def _generate_outputs(self) -> None:
        """Generate profiling and reporting outputs."""
        if self.enableProfile:
            generate_profile(self.data, self.version)
        generate_report(
            self.version, self.is_valid, self.error, self.timestamp, self.data
        )

    def _save_metadata(self) -> None:
        """Store metadata including previous version tracking."""
        self.previous = find_previous_version(self.version)
        save_metadata(self)
