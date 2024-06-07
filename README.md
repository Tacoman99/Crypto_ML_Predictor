## A real-time ML system that predicts short-term crypto prices

### Feature Pipeline

#### Trade producer (producer)
- [x] Fix the Dockerized trade producer
- [x] Share code with you 
- [ ] Add challenges for you to complete
- [x] Upload recordings.
- [x] Update the Dockerfile to avoid re-installing dependencies after changing the code.
- [x] Use logging instead of printing.
- [x] Add .env file with configuration, and remove the hard-coded values in the code.
- [x] Linting and formatting.

#### Trade to ohlc (transformation)
- [x] Dockerize
- [x] Makefile with build, run, lint and format commands
- [x] Load config parameters from env variables instead of hard-coding them

### Kafka to feature store (consumer)
- [ ] Dockerize
- [ ] Makefile with build, run, lint and format commands
- [ ] Load config parameters from env variables instead of hard-coding them

# Next steps
- [ ] Write a docker compose to run the whole feature pipeline locally.
- [ ] Backfill the feature group using historical data.
