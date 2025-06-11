from queue import Queue
from threading import Thread
from binance_ws import BinanceWebSocketListener
from stopLogic import StopManager
from prod import marlin_stop_logger
from prod.login import Login

def process_filled_stops(stop_filled_queue, stop_manager: StopManager):
    while True:
        order = stop_filled_queue.get()
        marlin_stop_logger.info(f"Processing filled stop order: {order}")
        stop_manager.register_filled_stop_order(order)
        stop_filled_queue.task_done()

def main():
    exchange_session = Login("binance")
    exchange_session.login_database()
    api_id = self.exchange_session.e_id
    api_key = self.exchange_session.e_sk

    stop_filled_queue = Queue()
    stop_manager = StopManager(api_id, api_key)
    ws_listener = BinanceWebSocketListener(api_key, stop_filled_queue)

    # Start the keep-alive thread for the listen key
    stop_event = Thread.Event()
    keepalive_thread = Thread(target=ws_listener.keepalive_listen_key, args=(api_key, ws_listener.listen_key, stop_event), daemon=True)
    keepalive_thread.start()

    # Start the WebSocket listener in a thread
    ws_thread = Thread(target=ws_listener.start, daemon=True)
    ws_thread.start()

    # Start the infinite loop processor
    processor_thread = Thread(target=process_filled_stops, args=(stop_filled_queue, stop_manager), daemon=True)
    processor_thread.start()

    marlin_stop_logger.info("Stop service running. Waiting for filled stop orders...")
    ws_thread.join()
    processor_thread.join()
    stop_event.set()  # Stop the keep-alive thread when exiting
    keepalive_thread.join()

if __name__ == "__main__":
    main()