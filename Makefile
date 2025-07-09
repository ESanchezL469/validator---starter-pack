VENVB_DIR := venv-backend
VENVF_DIR := venv-frontend

PYTHONB := $(VENVB_DIR)/bin/python
PYTHONF := $(VENVF_DIR)/bin/python

PYTEST := $(VENVB_DIR)/bin/pytest
PRE_COMMIT := $(VENVB_DIR)/bin/pre-commit

venv-backend:
	python3 -m venv $(VENVB_DIR)
	$(PYTHONB) -m pip install --upgrade pip

venv-frontend:
	python3 -m venv $(VENVF_DIR)
	$(PYTHONF) -m pip install --upgrade pip

venv: venv-backend venv-frontend

install-backend:
	$(VENVB_DIR)/bin/pip install --upgrade --force-reinstall -r app/requirements.txt

install-frontend:
	$(VENVF_DIR)/bin/pip install --upgrade --force-reinstall -r frontend/requirements.txt

install: install-backend install-frontend

clean:
	find . \( -type d -name '__pycache__' -o \
	           -type f -name '*.pyc' -o \
	           -type d -name '.pytest_cache' -o \
	           -type d -name '.mypy_cache' \) -exec rm -rf {} +

run-backend:
	PYTHONWARNINGS=ignore $(PYTHONB) -m app.run

run-ui:
	cd frontend && ../$(VENVF_DIR)/bin/streamlit run streamlit_app.py

test-unit:
	PYTHONPATH=. ${PYTEST} tests/unit -v

test-api:
	PYTHONPATH=. ${PYTEST} tests/integration -v

test-all:
	PYTHONPATH=. ${PYTEST} tests

coverage:
	PYTHONPATH=. ${PYTHONB} -m pytest --cov=app tests --cov-report=term-missing

activate-backend:
	@echo "Run this command to activate your environment:"
	@echo "source $(VENVB_DIR)/bin/activate"

activate-frontend:
	@echo "Run this command to activate your environment:"
	@echo "source $(VENVF_DIR)/bin/activate"

setup-pre-commit:
	$(PRE_COMMIT) install
	$(PRE_COMMIT) autoupdate

run-checks-backend: activate-backend
	$(PRE_COMMIT) run --all-files

run-checks-frontend:
	$(VENVF_DIR)/bin/black frontend
	$(VENVF_DIR)/bin/isort frontend
	$(VENVF_DIR)/bin/flake8 frontend

run-checks: run-checks-backend run-checks-frontend
