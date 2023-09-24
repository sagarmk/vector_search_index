.PHONY: build
build:
	docker-compose build

.PHONY: up
up:
	docker-compose up

.PHONY: down
down:
	docker-compose down

.PHONY: install
install:
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

.PHONY: run
run:
	streamlit run demo.py

.PHONY: style
style:
	isort . 
	black . 
	autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive . 

.PHONY: clean
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name ".DS_Store" -type f -delete
