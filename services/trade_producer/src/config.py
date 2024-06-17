from typing import List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings

# load my .env file variables as environment variables so I can access them
# with os.environ[] statements
# load_dotenv(find_dotenv())


class Config(BaseSettings):
    kafka_broker_address: Optional[str] = None
    kafka_topic: str
    # product_ids: List[str] = [
    #     'ETH/USD',
    #     # 'BTC/USD',
    #     # 'ETH/EUR',
    #     # 'BTC/EUR',
    #     # 'USDT/USD',
    #     # 'BNB/USD',
    #     # 'SOL/USD',
    #     # 'USDC/USD',
    #     # 'XRP/USD',
    # ]
    # product_ids: List[str] = ['ETH/USD']
    product_ids: List[str]

    # Challenge: validate that `live_or_historical` is either
    # 'live' or 'historical' using pydantic settings.
    live_or_historical: str = 'live'
    last_n_days: Optional[int] = 1

    @field_validator('live_or_historical')
    @classmethod
    def validate_live_or_historical(cls, value):
        assert value in {
            'live',
            'historical',
        }, f'Invalid value for live_or_historical: {value}'
        return value


config = Config()
