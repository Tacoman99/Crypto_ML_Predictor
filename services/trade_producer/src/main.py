from time import sleep
from typing import Dict, List

from loguru import logger
from quixstreams import Application

# from src import config
from src.config import config
from src.kraken_api import KrakenWebsocketTradeAPI


def produce_trades(
    kafka_broker_addres: str,
    kafka_topic_name: str,
    product_ids: List[str],
) -> None:
    """
    Reads trades from the Kraken websocket API and saves them into a Kafka topic.

    Args:
        kafka_broker_addres (str): The address of the Kafka broker.
        kafka_topic_name (str): The name of the Kafka topic.
        product_ids (List[str]): The product IDs for which we want to get the trades.

    Returns:
        None
    """
    app = Application(broker_address=kafka_broker_addres)

    # the topic where we will save the trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    logger.info(f'Creating the Kraken API to fetch data for {product_ids}')
    
    # Create an instance of the Kraken API
    kraken_api = KrakenWebsocketTradeAPI(product_ids=product_ids)

    logger.info('Creating the producer...')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            # Get the trades from the Kraken API
            trades: List[Dict] = kraken_api.get_trades()

            # Challenge 1: Send a heartbeat to Prometheus to check the service is alive
            # Challenge 2: Send an event with trade latency to Prometheus, to monitor the trade latency

            for trade in trades:
                # Serialize an event using the defined Topic
                message = topic.serialize(key=trade['product_id'], value=trade)

                # Produce a message into the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(trade)

            sleep(1)


if __name__ == '__main__':
    
    # You can also pass configuration parameters using the command line
    # use argparse to parse the kafka_broker_address
    # and kafka_topic_name from the command line
    # from argparse import ArgumentParser
    # parser = ArgumentParser()
    # parser.add_argument('--kafka_broker_address', type=str, required=False, default='localhost:9092')
    # parser.add_argument('--kafka_topic_name', type=str, required=True)
    # args = parser.parse_args()

    produce_trades(
        kafka_broker_addres=config.kafka_broker_addres,
        kafka_topic_name=config.kafka_topic_name,
        product_ids=config.product_ids,
    )
