import requests
from common.enums import Side_Type
from config.config import BASE_LOCAL_URL, STOP_LOSS_PERCENTAGE
from queue import Queue, Full
from common.constants import STOP_BUFFER_SIZE
import threading
from prod import marlin_stop_logger
from prod.binance import Binance
from typing import Dict

NEW_TRADE_ENDPOINT = "new_trade_stop"
ORDER_FILLED_ENDPOINT = "order_filled_stop"

class StopManager():
    """
    A class to handle stop order logic in a trading system.
    """

    def __init__(self, api_id, api_key):
        self.api_id = api_id
        self.api_key = api_key
        # The queue will hold dictionaries with the following structure:
        # {
        #     "side": Side_Type (enum),
        #     "value": float,
        #     "symbol": str,
        #     "quantity": float,
        #     "stop_price": float,
        #     "entry_price": float,
        #     "stop_loss_percentage": float
        # }
        self.stops_queue = Queue(maxsize=STOP_BUFFER_SIZE)
        self.thread = threading.Thread(target=self._process_from_queue, daemon=True)
        # self.thread.start()

    def _process_from_queue(self, order):
        """
        Process the order from the queue and create a stop order.

        Args:
            order (dict): A dictionary containing order details such as 'symbol', 'side', 'quantity', and 'stop_price'.

        Returns:
            dict: A dictionary containing the status of the stop order creation.
        """
        while True:
            stop_order, order_type = self.stops_queue.get()
            if order_type == "new_trade":
                req_url = BASE_LOCAL_URL + NEW_TRADE_ENDPOINT
            else:
                req_url = BASE_LOCAL_URL + ORDER_FILLED_ENDPOINT
            try:
                if os.getenv('ENVIRONMENT') == Environment_Place.AWS:
                    res = requests.post(req_url, data={stop_order})
                else:
                    print(f"Simulating request to {req_url} with data: {stop_order}")
            except requests.exceptions.RequestException as e:
                marlin_stop_logger.error(f"Error sending request to {req_url}: {e}")
                raise Exception(f"Error processing stop request: {e}")
            

    def create_stop_order(self, order: Dict, pair_precision) -> Dict:
        """
        Create a stop order based on the order already executed.
        Args:
            order (dict): A dictionary containing order details such as 'symbol', 'side', 'origQty', and 'price'.
            It's
        """
        marlin_stop_logger.info(f"Creating stop order for: {order}")
        stop_price = float(order["avgPrice"]) * \
            (1 - STOP_LOSS_PERCENTAGE / 100) if order["side"] == Side_Type.LONG else float(order["avgPrice"]) * \
            (1 + STOP_LOSS_PERCENTAGE / 100)

        stop_price = round(stop_price, pair_precision)

        marlin_stop_logger.info(f"Stop loss price calculated: {stop_price}")
        
        try:
            stop_order = Binance().create_stop_loss_order(
                symbol=order["symbol"],
                quantity=round(order["origQty"], pair_precision),
                side=order["side"],
                stop_loss_price=stop_price,
                b_id=self.api_id,
                b_sk=self.api_key
            )
            
            # TODO: checar codigo de retorno para saber se houve algum erro e notificar no telegram
            return stop_order
        except Exception as e:
            # TODO: notificar no telegram tambem
            return {"status": "error", "message": str(e)}

    def register_filled_stop_order(self, order):
        marlin_stop_logger.info(f"Order filled by stop: {order}")
        # TODO: Update database;
        # log
        # telegram