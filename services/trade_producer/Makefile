run-dev:
	KAFKA_BROKER_ADDRESS='localhost:19092' \
	source live.env && poetry run python src/main.py
	
run-dev-historical:
	KAFKA_BROKER_ADDRESS='localhost:19092' \
	source historical.env && poetry run python src/main.py

build:
	docker build -t trade-producer .

run: build
	docker run \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		trade-producer

lint:
	poetry run ruff check --fix

format:
	poetry run ruff format .

lint-and-format: lint format