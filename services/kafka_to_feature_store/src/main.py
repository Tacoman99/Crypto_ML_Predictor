from quixstreams import Application
from loguru import logger
import json

from src.hopsworks_api import push_data_to_feature_store

def kafka_to_feature_store(
    kafka_topic: str,
    kafka_broker_address: str,
    feature_group_name: str,
    feature_group_version: int,
) -> None:
    """
    Reads `ohlc` data from the Kafka topic and writes it to the feature store.
    More specifically, it writes the data to the feature group specified by
    - `feature_group_name` and `feature_group_version`.

    Args:
        kafka_topic (str): The Kafka topic to read from.
        kafka_broker_address (str): The address of the Kafka broker.
        feature_group_name (str): The name of the feature group to write to.
        feature_group_version (int): The version of the feature group to write to.

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group="kafka_to_feature_store",
    )

    # input_topic = app.topic(name=kafka_topic, value_serializer='json')

    # Create a consumer and start a polling loop
    with app.get_consumer() as consumer:
        consumer.subscribe(topics=[kafka_topic])

        while True:
            msg = consumer.poll(1)

            if msg is None:
                continue
            
            elif msg.error():
                logger.error('Kafka error:', msg.error())

                # If the message is an error, raise an exception
                # raise Exception('Kafka error:', msg.error())
                
                continue
            else:
                # there is data we need now to send to the feature store
                
                # step 1 -> parse the message from kafka into a dictionary
                ohlc = json.loads(msg.value().decode('utf-8'))

                # step 2 -> write the data to the feature store
                push_data_to_feature_store(
                    feature_group_name=feature_group_name,
                    feature_group_version=feature_group_version,
                    data=ohlc,
                )

                # breakpoint()

            # Store the offset of the processed message on the Consumer 
            # for the auto-commit mechanism.
            # It will send it to Kafka in the background.
            # Storing offset only after the message is processed enables at-least-once delivery
            # guarantees.
            consumer.store_offsets(message=msg)

if __name__ == '__main__':

    # Challenge: Load these values from the config.py file

    kafka_to_feature_store(
        kafka_topic='ohlc',
        kafka_broker_address='localhost:19092',
        feature_group_name='ohlc_feature_group',
        feature_group_version=1,
    )