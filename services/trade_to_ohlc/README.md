## Trade to ohlc service

This microservice

- Reads trades from a kafka topic
- Transforms them into OHLC candles, and
- Saves them in another kakfa topic