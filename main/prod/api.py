from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread, Event
# from prod.tradingBot import TradingBot
from prod.app import Main
import logging
from prod import api_logger
from prod import notify

api = FastAPI()

class Order(BaseModel):
    id: int
    item: str
    quantity: int

bot_ready = Event()
app = Main()

def start_main():
    try:
        bot_ready.set() # Signal that the bot is ready
        api_logger.debug(f"Bot ready status: {bot_ready.is_set()}")
        app.start()
    except Exception as e:
        api_logger.error(f"Error starting the bot: {e}")
        bot_ready.set() # Set the event even if error to prevent deadlock 

thread = Thread(target=start_main, daemon=True)
thread.start()

@api.get("/")
def index():
    if not bot_ready.is_set():
        return {"message": "Bot is starting..."}
    return {"message": "API ready and running"}

@api.post("/start")
async def start_app():
    if not bot_ready.is_set():
        notify.send_message_alert("Bot is starting......")
        return {"status": "Bot is starting..."}

    if hasattr(app, 'bot') and app.bot.running:
        return {"status": "App already running"}
    elif hasattr(app, 'bot'):
        app.bot.start()
        notify.send_message_alert("Bot started......")
        return {"status": "App started"}
    else:
        return {"status": "Bot not initialized"}

@api.post("/stop")
async def stop_app():
    api_logger.debug(f"stop endpoint called. Bot ready status: {bot_ready.is_set()}")
    if not bot_ready.is_set():
        return {"status": "Bot is already stopped......"}

    if hasattr(app, 'bot') and app.bot.running:
        app.bot.stop()
        notify.send_message_alert("Bot stopped......")
        return {"status": "App stopped"}
    else:
        return {"status": "App not running or bot not initialized"}

@api.get("/orders")
def get_orders():
    return orders

@api.get("/balance")
def get_balance():
    return {"balance": balance}

@api.get("/test") 
def test():
    return {"status": "OK"}