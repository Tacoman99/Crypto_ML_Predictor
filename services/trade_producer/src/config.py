from typing import List

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# load my .env file variables as environment variables so I can access them
# with os.environ[] statements
load_dotenv(find_dotenv())


class Config(BaseSettings):
    kafka_broker_address: str = 'localhost:19092'
    kafka_topic_name: str = 'trade'
    product_ids: List[str] = [
        'ETH/USD',
        'BTC/USD',
        'ETH/EUR',
        'BTC/EUR',
        # 'USDT/USD',
        # 'BNB/USD',
        # 'SOL/USD',
        # 'USDC/USD',
        # 'XRP/USD',
    ]
    # Challenge: validate that `live_or_historical` is either
    # 'live' or 'historical' using pydantic settings.
    live_or_historical: str = 'live'
    last_n_days: int = 1


config = Config()
