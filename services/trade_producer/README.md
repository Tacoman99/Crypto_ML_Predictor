# The trade producer service

## What does this service do?

This is the first step of our feature pipeline. This Python microservices

- reads trade events from the Kraken Websocket API, and
- saves them into a Kafka topic

## How to run this service?

### Step 1
To run this service locally you first need to start locally the message bus (Redpanda in this case).
```
$ cd ../../docker-compose && make start-redpanda
```

### Step 2
Build the Docker image for this service, and run the container
```
$ make run
```