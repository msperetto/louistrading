import requests
import threading
from queue import Queue, Full
from time import sleep
from dotenv import load_dotenv
import os
from prod import telegram_notify_logger
from common.secrets import get_secret


GROUP_ID_ALERTS = os.getenv("GROUP_ID_ALERTS")
GROUP_ID_OPERATION = os.getenv("GROUP_ID_OPERATION")
TELEGRAM_API_KEY = get_secret('TELEGRAM_API_KEY')

URL_BASE_ALERT = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage?chat_id={GROUP_ID_ALERTS}&parse_mode=html"
URL_BASE_OPERATION = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage?chat_id={GROUP_ID_OPERATION}&parse_mode=html"
TELEGRAM_BUFFER_SIZE = 40


class TelegramNotify:
    def __init__(self, buffer_size=TELEGRAM_BUFFER_SIZE):
        self.buffer_size = buffer_size
        self.message_buffer = Queue(maxsize=self.buffer_size)
        self.thread = threading.Thread(target=self._request_from_queue, daemon=True)
        self.thread.start()

    def _request_from_queue(self):
        while True:
            msg, msg_type = self.message_buffer.get()
            if msg_type == "alert":
                url_req = URL_BASE_ALERT
            elif msg_type == "operation":
                url_req = URL_BASE_OPERATION
            try:
                print(f"checking ENVIRONMENT varaible: {os.getenv('ENVIRONMENT')}")
                print(f"checking url utilized: {url_req}")
                if os.getenv('ENVIRONMENT') == 'production':
                    res = requests.post(url_req, data={"text": msg})
                    if res.status_code == 429:
                        retry_after = int(res.headers["Retry-After"])
                        telegram_notify_logger.error(
                            f"Getting Error 429 from Telegram API. Waiting {retry_after+1} seconds"
                        )
                        sleep(retry_after + 1)
                    elif res.status_code == 400:
                        # clean characters that break Telegram API
                        msg = msg.replace("<", "").replace(">", "")
                        res = requests.post(url_req, data={"text": msg})
                        # throw error if didn't work again
                        if res.status_code != 200:
                            telegram_notify_logger.error(
                                f"Getting error from Telegram API: {res.status_code} - {res.headers} - {res.content} - {msg}"
                            )
                            raise NameError("Telegram response not 200")
                    elif res.status_code != 200:
                        telegram_notify_logger.error(
                            f"Getting error from Telegram API: {res.status_code} - {res.headers} - {res.content} - {msg}"
                        )
                        raise NameError("Telegram response not 200")
                else:
                    print(msg)
            except Exception:
                telegram_notify_logger.error(f"Getting error from Telegram API.")
                raise NameError("Error on Telegram API request")

    def _send_message(self, msg):
        try:
            self.message_buffer.put(msg, block=False)
            print("colocando mensagem na fila")
        except Full:
            telegram_notify_logger.error(
                "Too many messages, can't handle. Deleting message buffer."
            )
            # resetting queue
            self.message_buffer = Queue(maxsize=self.buffer_size)
            self.message_buffer.put(
                ("Too many messages, deleting buffer.", "alert"), block=False
            )

        print(f"thread is alive: {self.thread.is_alive()}")

        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self._request_from_queue)
            self.thread.start()

    def send_message_alert(self, msg):
        msg = (msg, "alert")
        print("entrou send message alert")
        self._send_message(msg)

    def send_message_operation(self, msg):
        msg = (msg, "operation")
        self._send_message(msg)

    