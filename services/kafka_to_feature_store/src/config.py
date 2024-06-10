import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

# load my .env file variables as environment variables so I can access them
# with os.environ[] statements
load_dotenv(find_dotenv())

class Config(BaseSettings):
    
    kafka_broker_address: str = 'localhost:19092'
    kafka_topic: str
    feature_group_name: str
    feature_group_version: int
    buffer_size: int = 1

    # required to authenticate with Hopsworks API
    hopsworks_project_name: str
    hopsworks_api_key: str

config = Config()