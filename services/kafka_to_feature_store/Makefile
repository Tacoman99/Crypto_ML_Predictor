run-dev:
	KAFKA_BROKER_ADDRESS='localhost:19092' \
	source setup_credentials.sh && source setup_live_config.sh && poetry run python src/main.py

run-dev-historical:
	KAFKA_BROKER_ADDRESS='localhost:19092' \
	source setup_credentials.sh && source setup_historical_config.sh && poetry run python src/main.py

build:
	docker build -t kafka-to-feature-store .

run: build
	docker run \
		--network=redpanda_network \
		--env KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		--env KAFKA_TOPIC=ohlc \
		--env KAFKA_CONSUMER_GROUP=ohlc_consumer_group_99 \
		--env FEATURE_GROUP_NAME=ohlc_feature_group \
		--env FEATURE_GROUP_VERSION=1 \
		--env LIVE_OR_HISTORICAL=live \
		kafka-to-feature-store

lint:
	poetry run ruff check --fix

format:
	poetry run ruff format .

lint-and-format: lint format