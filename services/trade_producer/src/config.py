
import os
from typing import List

from dotenv import find_dotenv, load_dotenv

# load my .env file variables as environment variables so I can access them
# with os.environ[] statements
load_dotenv(find_dotenv())

# product_id = 'ETH/USD'
# kafka_broker_addres = os.environ['KAFKA_BROKER_ADDRESS']
# kafka_topic_name='trade'

from pydantic_settings import BaseSettings


class Config(BaseSettings):
<<<<<<< HEAD
    product_id: str = 'ETH/EUR'
=======
    product_ids: List[str] = ['ETH/USD', 'BTC/USD', 'ETH/EUR', 'BTC/EUR']
>>>>>>> a53b3a4 (Support for multiple product_ids in trade-producer)
    kafka_broker_addres: str = os.environ['KAFKA_BROKER_ADDRESS']
    kafka_topic_name: str = 'trade'
    # ohlc_windows_seconds: int = os.environ['OHLC_WINDOWS_SECONDS']

config = Config()