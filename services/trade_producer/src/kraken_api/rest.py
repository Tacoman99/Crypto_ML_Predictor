from typing import List, Dict


class KrakenRestAPI:

    URL = "https://api.kraken.com/0/public/Trades?pair={product_id}&since={since_ms}"

    def __init__(
        self,
        product_ids: List[str],
        from_ms: int,
        to_ms :int
    ) -> None:
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
        url = self.URL.format(product_id=self.product_ids[0], since_ms=self.from_ms)

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

        # parse string into dictionary
        import json
        data = json.loads(response.text)
        
        breakpoint()

    def is_done(self) -> bool:
        return False