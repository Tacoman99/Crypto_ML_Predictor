# These are the environment variables we will need to set to run
# the trade_producer in historical mode in Quix Cloud
export KAFKA_TOPIC=trade_historical
export PRODUCT_IDS='["ETH/USD","BTC/USD","BTC/EUR","USDT/USD","USDT/USD"]'
export LIVE_OR_HISTORICAL=historical
export LAST_N_DAYS=90