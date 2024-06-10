import json
from typing import Dict, List

from loguru import logger
from websocket import create_connection


class KrakenWebsocketTradeAPI:
    URL = 'wss://ws.kraken.com/v2'

    def __init__(
        self,
        product_ids: List[str],
    ):
        self.product_ids = product_ids

        # establish connection to the Kraken websocket API
        self._ws = create_connection(self.URL)
        logger.info('Connection established')

        # subscribe to the trades for the given `product_id`
        self._subscribe(product_ids)

    def _subscribe(self, product_ids: List[str]):
        """
        Establish connection to the Kraken websocket API and subscribe to the trades for the given `product_id`.
        """
        logger.info(f'Subscribing to trades for {product_ids}')
        # let's subscribe to the trades for the given `product_id`
        msg = {
            'method': 'subscribe',
            'params': {
                'channel': 'trade',
                'symbol': product_ids,
                'snapshot': False,
            },
        }
        self._ws.send(json.dumps(msg))
        logger.info('Subscription worked!')

        # For each product_id we dump
        # the first 2 messages we got from the websocket, because they contain
        # no trade data, just confirmation on their end that the subscription was successful
        for product_id in product_ids:
            _ = self._ws.recv()
            _ = self._ws.recv()

    def get_trades(self) -> List[Dict]:
        message = self._ws.recv()

        if 'heartbeat' in message:
            # when I get a heartbeat, I return an empty list
            return []

        # parse the message string as a dictionary
        message = json.loads(message)

        # extract trades from the message['data'] field
        trades = []
        for trade in message['data']:
            trades.append(
                {
                    'product_id': trade['symbol'],
                    'price': trade['price'],
                    'volume': trade['qty'],
                    'timestamp': trade['timestamp'],
                }
            )

        # breakpoint()

        return trades

    def is_done(self) -> bool:
        """The websocket never stops, so we never stop fetching trades."""
        return False