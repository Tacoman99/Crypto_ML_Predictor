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
- [x] Dockerize
- [x] Makefile with build, run, lint and format commands
- [x] Load config parameters from env variables instead of hard-coding them

# Next steps
- [x] Write a docker compose to run the whole feature pipeline locally.
    - [x] Pay attention to the network.
- [ ] Backfill the feature group using historical data.
    - [x] Adjust trade producer to connect to Kraken's REST API
    - [ ] Adjust `kafka_to_feature_store` to save data to the offline feature group.
        - [ ] Make sure we write the data to the offline feature group. The code as it is now
        saves a batch of features (not just one, which is great) but to the online store.

- [ ] Package the entire backfill pipeline with docker compose, run it and check we have the data we need in Hopsworks.


## My TODOs
- [x] Fix bug when retrieving historical data. At the moment we fetch the first batch of 1000 trades again and again.
- [x] How to fetch historical data for multiple product_ids at the same time.
- [x] Emit ohlc events at the end only.
- [x] Run the backfill pipeline for the last 1 year.
- [x] Fix timestamps for websocket and historical mode.
- [x] Extract config in .env files, except from the KAFKA_BROKER_ADDRES
- [x] Fix bug in the trade_producer, where timestamps are not consistently named in websocket.py vs rest.pi.
- [x] Add cache to speed things up.
- [x] Add caching to docker compose
- [x] BTC/USD gets stuck at 18:33
- [x] Prepare slides -> Streamlit app
- [x] Finish dashboard to check historical data is in the Store
- [ ] Create a tools package and do the following:
    - [x] Write a script to read historical features from the stoer -> OhlcDataReader
    - [x] Write a script to download this parquet file and push it to a given feature_group

- [ ] Slides modle training
    ohlc data
    missing value interpolation
    target definition
    feature engineering
    baseline model
    lightgbm model
    hyperparameter tuning.