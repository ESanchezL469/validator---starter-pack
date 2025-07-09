VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

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
	PYTHONPATH=. pytest tests/unit -v

test-api:
	PYTHONPATH=. pytest tests/integration -v

test-all:
	PYTHONPATH=. pytest tests

coverage:
	PYTHONPATH=. ${PYTHON} --cov=app tests --cov-report=term-missing

activate:
	@echo "Run this command to activate your environment:"
	@echo "source $(VENV_DIR)/bin/activate"

setup-pre-commit:
	pre-commit install
	pre-commit autoupdate

run-checks:
	pre-commit run --all-files
