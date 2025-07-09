VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
PYTEST := $(VENV_DIR)/bin/pytest
PRE_COMMIT := $(VENV_DIR)/bin/pre-commit

venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip

install: venv
	${PIP} install -r requirements.txt --upgrade --force-reinstall

clean:
	find . -type d -name '__pycache__' -exec rm -r {} + && \
	find . -type f -name '*.pyc' -delete && \
	find . -type d -name '.pytest_cache' -exec rm -r {} + && \
	find . -type d -name '.mypy_cache' -exec rm -r {} +

run:
	PYTHONWARNINGS=ignore ${PYTHON} run.py

test-unit:
	PYTHONPATH=. ${PYTEST} tests/unit -v

test-api:
	PYTHONPATH=. ${PYTEST} tests/integration -v

test-all:
	PYTHONPATH=. ${PYTEST} tests

coverage:
	PYTHONPATH=. ${PYTHON} --cov=app tests --cov-report=term-missing

activate:
	@echo "Run this command to activate your environment:"
	@echo "source $(VENV_DIR)/bin/activate"

setup-pre-commit:
	pre-commit install
	pre-commit autoupdate

run-checks:
	${PRE_COMMIT} run --all-files
