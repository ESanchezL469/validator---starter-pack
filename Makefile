# Makefile - Validator - Starter Pack
INPUT ?= ""
FOLDER ?= "."
PROFILE ?= false

install:
	pip install -r requirements.txt --upgrade --force-reinstall

clean:
	find . -type d -name '__pycache__' -exec rm -r {} + && \
	find . -type f -name '*.pyc' -delete && \
	rm -rf .pytest_cache 

run:
	PYTHONWARNINGS=ignore python run.py

test-unit:
	PYTHONPATH=. pytest tests/unit -v

test-api:
	PYTHONPATH=. pytest tests/integration -v

test-all:
	PYTHONPATH=. pytest tests

docker-build:
	docker build -t dataops-validator .

docker-run:
	docker run -it \
		-v $(PWD)/datasets:/app/datasets \
		-v $(PWD)/reports:/app/reports \
		-v $(PWD)/metadata:/app/metadata \
		dataops-validator

coverage:
	PYTHONPATH=. pytest --cov=app tests --cov-report=term-missing