# Makefile - DataOps Starter Kit

install:
	pip install -r requirements.txt

run:
	PYTHONPATH=. python app/main.py

test:
	pytest tests/

docker-build:
	docker build -t dataops-validator .

docker-run:
	docker run -it \
		-v $(PWD)/datasets:/app/datasets \
		-v $(PWD)/reports:/app/reports \
		-v $(PWD)/metadata:/app/metadata \
		dataops-validator
