# The trade producer service

## What does this service do?

This is the first step of our feature pipeline. This Python microservices

- reads trade events from the Kraken Websocket API, and
- saves them into a Kafka topic