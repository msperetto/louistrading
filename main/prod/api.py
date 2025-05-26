from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread, Event
# from prod.tradingBot import TradingBot
from prod.app import Main
import logging
from prod import api_logger
from prod import notify
from common.dao.database_operations import get_initial_config, get_bot_execution_control, get_active_pairs
from common.dao.trade_dao import get_open_trade_pairs
from common.dao.alert_dao import get_active_alerts
from common.dao.account_balance_dao import get_account_balance
from common.domain.trade import Trade
from common.domain.alert import Alert
from common.domain.account_balance import AccountBalance
from config.config import ACCOUNT_ID
from time import sleep

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

@api.post("/hardreset")
async def hardreset():
    try:
        import os

        if hasattr(app, 'bot') and app.bot.running:
            api_logger.debug(f"initializing hard reset in api.py")
            app.bot.stop()
            notify.send_message_alert("Bot stopped...")
            api_logger.debug(f"bot.stopped status: {app.bot.stopped}")
            while not app.bot.stopped:
                api_logger.debug(f"bot.stopped inside while loop: {app.bot.stopped}")
                sleep(0.5)
            
            notify.send_message_alert("Attempting to hard reset...")
            os._exit(1)
            return {"status": "attempting to hard reset...", "error": False}
    except Exception as e:
        api_logger.error(f"Error during hard reset: {e}")
        return {"status": f"Error during hard reset: {e}", "error": True}

            

@api.get("/status")
async def status():
    response = {}
    initial_config = get_initial_config()
    bot_execution_control = get_bot_execution_control()
    active_pairs = get_active_pairs()
    open_trades_pairs = get_open_trade_pairs()
    account_balance = get_account_balance(ACCOUNT_ID)
    response["enabled"] = initial_config["opperation_active"]
    response["max_open_orders"] = initial_config["max_open_orders"]
    response["order_value"] = initial_config["order_value"]
    response["leverage_long"] = initial_config["leverage_long_value"]
    response["leverage_short"] = initial_config["leverage_short_value"]
    response["last_execution"] = bot_execution_control["last_execution"]
    response["open_trade_pairs"] = [trade.pair for trade in open_trades_pairs]
    response["open_trade_quantity"] = len(open_trades_pairs)
    response["active_pairs"] = active_pairs
    response["balance"] = round(account_balance.account_balance, 2)
    if not bot_ready.is_set():
        response["current_state"] = "Bot is starting..."
    if hasattr(app, 'bot') and app.bot.running:
        response["current_state"] = "App running"
    else:
        response["current_state"] = "App not running or bot not initialized"

    return response

@api.get("/active_alerts")
async def active_alerts():
    response = []
    active_alerts = get_active_alerts()
    for alert in active_alerts:
        response.append(
            {"pair": alert.pair, "alert_type": alert.alert_type, "date": alert.date, "message": alert.message}
        )
    return response

@api.get("/account/balance")
async def account_balance():
    response = {}
    account_balance = get_account_balance(ACCOUNT_ID)
    response = {
        "balance": account_balance.account_balance,
        "margin_ratio": account_balance.margin_ratio,
        "date_updated": account_balance.date_updated,
    }
    return response

@api.get("/orders")
def get_orders():
    return orders

@api.get("/balance")
def get_balance():
    return {"balance": balance}

@api.get("/test") 
def test():
    return {"status": "OK"}