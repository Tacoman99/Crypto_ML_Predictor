
import os
from dotenv import load_dotenv, find_dotenv

# load my .env file variables as environment variables so I can access them
# with os.environ[] statements
load_dotenv(find_dotenv())

# product_id = 'ETH/USD'
# kafka_broker_addres = os.environ['KAFKA_BROKER_ADDRESS']
# kafka_topic_name='trade'

from pydantic_settings import BaseSettings

class Config(BaseSettings):
    product_id: str = 'ETH/EUR'
    kafka_broker_addres: str = os.environ['KAFKA_BROKER_ADDRESS']
    kafka_topic_name: str = 'trade'
    ohlc_windows_seconds: int = os.environ['OHLC_WINDOWS_SECONDS']

config = Config()