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

    def __init__(self, setup, pair, pair_price_precision=0, api_id=None, api_key=None):
        self.setup = setup
        self.pair = pair
        self.pair_price_precision = pair_price_precision
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
        self.thread = threading.Thread(
            target=self._process_from_queue, daemon=True)
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
                    print(
                        f"Simulating request to {req_url} with data: {stop_order}")
            except requests.exceptions.RequestException as e:
                marlin_stop_logger.error(
                    f"Error sending request to {req_url}: {e}")
                raise Exception(f"Error processing stop request: {e}")

    def create_stop_order(self, order: Dict, pair_precision: int) -> Dict:
        """
        Create a stop order based on the order already executed.
        Args:
            order (dict): A dictionary containing order details such as 'symbol', 'side', 'origQty', and 'price'.
            It's
        """
        marlin_stop_logger.info(f"Creating stop order for: {order}")
        avg_price = float(order["avgPrice"])
        quantity = round(float(order["origQty"]), pair_precision)
        original_side = order["side"]
        stop_side = Side_Type.LONG.value if original_side == Side_Type.SHORT.value else Side_Type.SHORT.value

        try:
            stop_price = self._calculate_stop_price(
                avg_price,
                original_side,
                self.setup.stop_loss_percentage,
                self.pair_price_precision
            )

            marlin_stop_logger.info(
                f"Stop price calculated: {stop_price}; Side_type.long.value: {Side_Type.LONG.value}, pair_precision: {pair_precision}")

            stop_order = Binance().create_stop_loss_order(
                symbol=order["symbol"],
                quantity=quantity,
                side=stop_side,
                stop_loss_price=stop_price,
                b_id=self.api_id,
                b_sk=self.api_key
            )
            marlin_stop_logger.info(f"Stop order created: {stop_order}")

            return stop_order

        except Exception as e:
            marlin_stop_logger.error(f"Error creating stop order: {e}")
            # TODO: notificar no telegram tambem
            return {"status": "error", "message": str(e)}

    def check_closed_stop_order(self, symbol, startTime=0):
        """
        Check if there are any closed stop orders for the given symbol.

        Args:
            symbol (str): The trading pair symbol to check for closed stop orders.

        Returns:
            list: A list of closed stop orders for the given symbol.
        """
        try:
            marlin_stop_logger.debug(f"Checking closed stop orders for symbol: {symbol} with startTime: {startTime}")
            closed_orders = Binance().query_account_trade_list(
                symbol=self.pair, startTime=startTime, b_id=self.api_id, b_sk=self.api_key)
            marlin_stop_logger.debug(f"Closed orders for {symbol}: {closed_orders}")
            return closed_orders
        except Exception as e:
            marlin_stop_logger.error(f"Error checking closed stop orders: {e}")
            return []

    def register_filled_stop_order(self, order):
        marlin_stop_logger.info(f"Order filled by stop: {order}")
        # TODO: Update database;
        # log
        # telegram

    def _calculate_stop_price(self, avg_price: float, side: str, stop_loss_percentage: float, price_precision: int) -> float:
        """
        Calculate the stop price based on the average entry price, side of the trade, and stop loss percentage.
        Args:
            avg_price (float): average price.
            side (str): 'LONG' or 'SHORT' (Side_Type.value).
            stop_loss_percentage (float): stop percentage (ex: 0.01 para 1%).
            price_precision (int): decimal places precision for the price.

        Returns:
            float: rounded stop price.
        """
        if side == Side_Type.LONG.value:
            stop_price = avg_price * (1 - stop_loss_percentage)
        elif side == Side_Type.SHORT.value:
            stop_price = avg_price * (1 + stop_loss_percentage)
        else:
            raise ValueError(f"Invalid side: {side}")

        return round(stop_price, price_precision)
