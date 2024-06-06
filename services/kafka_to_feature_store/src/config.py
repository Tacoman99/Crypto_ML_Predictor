import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

# load my .env file variables as environment variables so I can access them
# with os.environ[] statements
load_dotenv(find_dotenv())

class Config(BaseSettings):
    
    # Challenge: add the other ones here
    # kafka_broker_addres: str = os.environ['KAFKA_BROKER_ADDRESS']
    # kafka_topic_name: str = 'trade'
    # ohlc_windows_seconds: int = os.environ['OHLC_WINDOWS_SECONDS']

    # I am just gonna do the real secret ones to work with Hopsworks
    hopsworks_project_name: str = os.environ['HOPSWORKS_PROJECT_NAME']
    hopsworks_api_key: str = os.environ['HOPSWORKS_API_KEY']

config = Config()