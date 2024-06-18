## Trade to ohlc service

This microservice

- Reads trades from a kafka topic
- Transforms them into OHLC candles, and
- Saves them in another kakfa topic

## How to run this service?

## Set up
To run this service locally you first need to start locally the message bus (Redpanda in this case).
```
$ cd ../../docker-compose && make start-redpanda
```

### Without Docker

In live mode
```
$ make run-dev
```

In historical mode (for backfills)
```
$ make run-dev-historical
```

### With Docker

Build the Docker image and run the service in live mode
```
$ make run
```

Build the Docker image and run the service in historical mode
```
$ make run-historical
```
