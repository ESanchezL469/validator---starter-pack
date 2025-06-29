# Makefile - DataOps Starter Kit

INPUT ?= ""
FOLDER ?= "."
PROFILE ?= false

install:
	pip install -r requirements.txt

run:
	PYTHONPATH=. python app/main.py \
		$(if $(filter-out false,$(PROFILE)),--profile,) \
		$(if $(INPUT),--input=$(INPUT),) \
		$(if $(filter-out .,$(FOLDER)),--input-folder "$(FOLDER)",)

test:
	PYTHONPATH=. pytest tests/

docker-build:
	docker build -t dataops-validator .

docker-run:
	docker run -it \
		-v $(PWD)/datasets:/app/datasets \
		-v $(PWD)/reports:/app/reports \
		-v $(PWD)/metadata:/app/metadata \
		dataops-validator
