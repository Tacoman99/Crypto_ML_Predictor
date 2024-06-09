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


config = Config()
