import json
from typing import Optional

from loguru import logger
from quixstreams import Application

from src.hopsworks_api import push_data_to_feature_store


def get_current_utc_sec() -> int:
    """
    Returns the current UTC time expressed in seconds since the epoch.

    Args:
        None

    Returns:
        int: The current UTC time expressed in seconds since the epoch.
    """
    from datetime import datetime, timezone

    return int(datetime.now(timezone.utc).timestamp())


def kafka_to_feature_store(
    kafka_topic: str,
    kafka_broker_address: str,
    kafka_consumer_group: str,
    feature_group_name: str,
    feature_group_version: int,
    buffer_size: Optional[int] = 1,
    live_or_historical: Optional[str] = 'live',
    save_every_n_sec: Optional[int] = 600,
) -> None:
    """
    Reads `ohlc` data from the Kafka topic and writes it to the feature store.
    More specifically, it writes the data to the feature group specified by
    - `feature_group_name` and `feature_group_version`.

    Args:
        kafka_topic (str): The Kafka topic to read from.
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_consumer_group (str): The Kafka consumer group we use for reading messages.
        feature_group_name (str): The name of the feature group to write to.
        feature_group_version (int): The version of the feature group to write to.
        buffer_size (int): The number of messages to read from Kafka before writing to the feature store.
        live_or_historical (str): Whether we are saving live data to the Feature or historical data.
            Live data goes to the online feature store
            While historical data goes to the offline feature store.
        save_every_n_sec (int): The max seconds to wait before writing the data to the
            feature store.

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        # auto_offset_reset="earliest" if live_or_historical == 'historical' else "latest",
        auto_offset_reset='latest',
    )

    # get current UTC time in seconds
    last_saved_to_feature_store_ts = get_current_utc_sec()

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

            # number of seconds since the last time we saved data to the feature store
            sec_since_last_saved = (
                get_current_utc_sec() - last_saved_to_feature_store_ts
            )

            if (msg is not None) and msg.error():
                # We have a message but it is an error.
                # We just log the error and continue
                logger.error('Kafka error:', msg.error())
                continue

            elif (msg is None) and (sec_since_last_saved < save_every_n_sec):
                # There are no new messages in the input topic and we haven't hit the timer
                # limit yet. We skip and continue polling messages from Kafka.
                logger.debug('No new messages in the input topic')
                logger.debug(
                    f'Last saved to feature store {sec_since_last_saved} seconds ago'
                )
                logger.debug(f'We have not hit the {save_every_n_sec} second limit.')
                continue

            else:
                # either we have a message or we have hit the timer limit
                # if we have a message we need to add it to the buffer
                if msg is not None:
                    # append the data to the buffer
                    ohlc = json.loads(msg.value().decode('utf-8'))
                    buffer.append(ohlc)
                    logger.debug(
                        f'Message was pushed to buffer. Buffer size={len(buffer)}'
                    )

                    # # Store the offset of the processed message on the Consumer
                    # # for the auto-commit mechanism.
                    # # It will send it to Kafka in the background.
                    # # Storing offset only after the message is processed enables at-least-once delivery
                    # # guarantees.
                    # consumer.store_offsets(message=msg)

                # if the buffer is full or we have hit the timer limit,
                # we write the data to the feature store
                if (len(buffer) >= buffer_size) or (
                    sec_since_last_saved >= save_every_n_sec
                ):
                    # if the buffer is not empty we write the data to the feature store
                    if len(buffer) > 0:
                        try:
                            push_data_to_feature_store(
                                feature_group_name=feature_group_name,
                                feature_group_version=feature_group_version,
                                data=buffer,
                                online_or_offline='online'
                                if live_or_historical == 'live'
                                else 'offline',
                            )
                        except Exception as e:
                            logger.error(
                                f'Failed to push data to the feature store: {e}'
                            )
                            continue

                        # reset the buffer
                        # Thanks Rosina!
                        buffer = []

                        last_saved_to_feature_store_ts = get_current_utc_sec()


if __name__ == '__main__':
    from src.config import config

    logger.debug(config.model_dump())

    try:
        kafka_to_feature_store(
            kafka_topic=config.kafka_topic,
            kafka_broker_address=config.kafka_broker_address,
            kafka_consumer_group=config.kafka_consumer_group,
            feature_group_name=config.feature_group_name,
            feature_group_version=config.feature_group_version,
            buffer_size=config.buffer_size,
            live_or_historical=config.live_or_historical,
            save_every_n_sec=config.save_every_n_sec,
        )
    except KeyboardInterrupt:
        logger.info('Exiting neatly!')
