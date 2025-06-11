import asyncio
import json
import websockets
from queue import Queue
from threading import Thread
from prod import marlin_stop_logger

class BinanceWebSocketListener:
    BINANCE_API_URL = "https://fapi.binance.com"
    BINANCE_WS_URL = "wss://fstream.binance.com/ws"
    LISTEN_KEY_ENDPOINT = "/fapi/v1/listenKey"
    KEEP_ALIVE_INTERVAL = 1800  # 30 minutes

    def __init__(self, api_key, stop_filled_queue: Queue):
        self.listen_key = self._get_listen_key(self.api_key)
        self.ws_url = f"{BINANCE_WS_URL}/{self.listen_key}"
        self.stop_filled_queue = stop_filled_queue
        self.running = False

    def _get_listen_key(api_key):
        headers = {"X-MBX-APIKEY": api_key}
        resp = requests.post(f"{self.BINANCE_API_URL+self.LISTEN_KEY_ENDPOINT}", headers=headers)
        resp.raise_for_status()
        return resp.json()["listenKey"]

    def keepalive_listen_key(api_key, listen_key, stop_event):
        headers = {"X-MBX-APIKEY": api_key}
        while not stop_event.is_set():
            try:
                resp = requests.put(f"{self.BINANCE_API_URL+self.LISTEN_KEY_ENDPOINT}", headers=headers, params={"listenKey": listen_key})
                if resp.status_code == 200:
                    print("Listen key refreshed.")
                else:
                    print(f"Failed to refresh listen key: {resp.text}")
            except Exception as e:
                print(f"Error refreshing listen key: {e}")
            stop_event.wait(self.KEEP_ALIVE_INTERVAL)

    async def _listen(self):
        marlin_stop_logger.info("Starting Binance WebSocket listener...")
        async with websockets.connect(self.ws_url) as ws:
            self.running = True
            while self.running:
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    # Listen for order trade updates
                    if data.get("e") == "ORDER_TRADE_UPDATE":
                        order = data["o"]
                        # Check if it's a STOP_MARKET order and filled
                        if order.get("type") == "STOP_MARKET" and order.get("X") == "FILLED":
                            marlin_stop_logger.info(f"Stop order filled: {order}")
                            self.stop_filled_queue.put(order)
                except Exception as e:
                    marlin_stop_logger.error(f"WebSocket error: {e}")
                    await asyncio.sleep(5)  # Reconnect delay

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._listen())

    def stop(self):
        self.running = False