from typing import List, Dict
import json

from loguru import logger


class KrakenRestAPI:
    URL = 'https://api.kraken.com/0/public/Trades?pair={product_id}&since={since_sec}'

    def __init__(self, product_ids: List[str], from_ms: int, to_ms: int) -> None:
        """
        Basic initialization of the Kraken Rest API.

        Args:
            product_ids (List[str]): A list of product IDs for which we want to get the trades.
            from_ms (int): The start timestamp in milliseconds.
            to_ms (int): The end timestamp in milliseconds.

        Returns:
            None
        """
        self.product_ids = product_ids
        self.from_ms = from_ms
        self.to_ms = to_ms

        logger.debug(f'Initializing KrakenRestAPI: from_ms={from_ms}, to_ms={to_ms}')

        # breakpoint()

        # the timestamp from which we want to fetch historical data
        # this will be updated after each batch of trades is fetched from the API
        # self.since_ms = from_ms
        self.last_trade_ms = from_ms

        # are we done fetching historical data?
        # Yes, if the last batch of trades has a data['result'][product_id]['last'] >= self.to_ms
        self._is_done = False

    def get_trades(self) -> List[Dict]:
        """
        Fetches a batch of trades from the Kraken Rest API and returns them as a list
        of dictionaries.

        Args:
            None

        Returns:
            List[Dict]: A list of dictionaries, where each dictionary contains the trade data.
        """
        import requests

        payload = {}
        headers = {'Accept': 'application/json'}

        # replacing the placeholders in the URL with the actual values for
        # - product_id
        # - since_ms
        since_sec = self.last_trade_ms // 1000
        url = self.URL.format(product_id=self.product_ids[0], since_sec=since_sec)

        response = requests.request('GET', url, headers=headers, data=payload)

        # parse string into dictionary
        data = json.loads(response.text)

        # TODO: check if there is an error in the response, right now we don't do any
        # error handling
        # if data['error'] is not []:
        #     # if there is an error, raise an exception
        #     raise Exception(data['error'])

        # trades = []
        # for trade in data['result'][self.product_ids[0]]:
        #     trades.append({
        #         'price': float(trade[0]),
        #         'volume': float(trade[1]),
        #         'time': int(trade[2]),
        #     })

        # little trick. Instead of initializing an empty list and appending to it, you
        # can use a list comprehension to do the same thing
        trades = [
            {
                'price': float(trade[0]),
                'volume': float(trade[1]),
                'time': int(trade[2]),
                'product_id': self.product_ids[0],
            }
            for trade in data['result'][self.product_ids[0]]
        ]

        # filter out trades that are after the end timestamp
        trades = [trade for trade in trades if trade['time'] <= self.to_ms // 1000]

        # check if we are done fetching historical data
        last_ts_in_ns = int(data['result']['last'])
        self.last_trade_ms = last_ts_in_ns // 1_000_000
        self._is_done = self.last_trade_ms >= self.to_ms

        # breakpoint()

        logger.debug(f'Fetched {len(trades)} trades')
        # log the last trade timestamp
        logger.debug(f'Last trade timestamp: {self.last_trade_ms}')

        # breakpoint()

        return trades

    def is_done(self) -> bool:
        return self._is_done
        # return self.since_ms >= self.to_ms
