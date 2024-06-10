from quixstreams import Application
from loguru import logger
import json

from src.hopsworks_api import push_data_to_feature_store

def kafka_to_feature_store(
    kafka_topic: str,
    kafka_broker_address: str,
    feature_group_name: str,
    feature_group_version: int,
    buffer_size: int = 1,
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
        buffer_size (int): The number of messages to read from Kafka before writing to the feature store.

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group="kafka_to_feature_store",
        # auto_offset_reset="earliest",
    )

    # input_topic = app.topic(name=kafka_topic, value_serializer='json')

    # contains the list of trades to be written to the feature store at once
    # TODO: handle the case where there the last batch is not full but no more data is
    # coming. With the current implementation we can have up to (buffer_size - 1) messages
    # in the buffer that will never be written to the feature store.
    buffer = []

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

                # append the data to the buffer
                buffer.append(ohlc)

                # breakpoint()

                # if the buffer is full, write the data to the feature store
                if len(buffer) >= buffer_size:
                    
                    # step 2 -> write the data to the feature store
                    push_data_to_feature_store(
                        feature_group_name=feature_group_name,
                        feature_group_version=feature_group_version,
                        data=buffer,
                    )

                    # reset the buffer
                    buffer = []

                # # step 2 -> write the data to the feature store
                # push_data_to_feature_store(
                #     feature_group_name=feature_group_name,
                #     feature_group_version=feature_group_version,
                #     data=ohlc,
                # )

                # breakpoint()

            # Store the offset of the processed message on the Consumer 
            # for the auto-commit mechanism.
            # It will send it to Kafka in the background.
            # Storing offset only after the message is processed enables at-least-once delivery
            # guarantees.
            consumer.store_offsets(message=msg)

if __name__ == '__main__':

    from src.config import config
    logger.debug(config.model_dump())

    try:
        kafka_to_feature_store(
            kafka_topic=config.kafka_topic,
            kafka_broker_address=config.kafka_broker_address,
            feature_group_name=config.feature_group_name,
            feature_group_version=config.feature_group_version,
            buffer_size=config.buffer_size,
        )
    except KeyboardInterrupt:
        logger.info('Exiting neatly!')