import logging
import requests
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
from dotenv import load_dotenv
import os
from common.util import get_server_public_ip
from common.secrets import get_secret
from prod import telegram_logger
from common.enums import Environment_Place
from common.dao.trade_dao import get_open_trade_by_pair
from common.domain.trade import Trade
from datetime import datetime

if os.getenv('ENVIRONMENT') != Environment_Place.AWS:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)  # Ensure environment variables are loaded from .env file
    BASE_LOCAL_URL = "http://localhost:8000/"
    telegram_logger.info(f"Development mode: Using {BASE_LOCAL_URL}")
else:
    EC2_IP = get_server_public_ip("EC2_PUBLIC_IP")
    if not EC2_IP:
        raise ValueError("Unable to retrieve EC2 public IP")
    BASE_LOCAL_URL = f"http://{EC2_IP}:8000/"

TELEGRAM_API_KEY = get_secret('TELEGRAM_API_KEY')
BASE_URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_API_KEY)
MAX_MESSAGE_LEN = 4096

def get_request(endpoint):
    url = BASE_LOCAL_URL + endpoint
    response = requests.get(url).json()
    return response


def post_request(endpoint, data=None):
    url = BASE_LOCAL_URL + endpoint
    response = requests.post(url, data=data).json()
    return response


def start(update, context):
    try:
        response = post_request("start")
        # Check if response contains status key
        message = response.get('status', 'Unknown response')
        update.message.reply_text(message, parse_mode=ParseMode.HTML)
    except Exception as e:
        telegram_logger.error(f"Error starting the bot: {e}")
        update.message.reply_text("Error starting the bot", parse_mode=ParseMode.HTML)


def stop(update, context):
    try:
        response = post_request("stop")
        # Check if response contains status key
        message = response.get('status', 'Unknown response')
        update.message.reply_text(message, parse_mode=ParseMode.HTML)
    except Exception as e:
        telegram_logger.error(f"Error stopping the bot: {e}")
        update.message.reply_text("Error stopping the bot", parse_mode=ParseMode.HTML)


def hard_reset(update, context):
    try:
        response = post_request("hard_reset")
        # Check if response contains status key
        message = response.get('msg', 'Unknown response')
        update.message.reply_text(message, parse_mode=ParseMode.HTML)
    except Exception as e:
        telegram_logger.error(f"Error hard resetting the bot: {e}")
        update.message.reply_text("Error hard resetting the bot", parse_mode=ParseMode.HTML)


def help(update, context):
    msg = "<b>Available commands:</b>\n\n"
    msg += "/start - Start the bot\n"
    msg += "/stop - Stop the bot\n"
    msg += "/status - Get the bot status\n"
    msg += "/active_alerts - Get active alerts\n"
    msg += "/hard_reset - Hard reset the bot\n"
    msg += "/help - Show this help message\n"
    update.message.reply_text(msg, parse_mode=ParseMode.HTML)


def status(update, context):
    try:
        response = get_request("status")
        msg = f"<b>Status:</b>\n"
        msg += f"Bot enabled: {response.get('enabled', 'Unknown')}\n"
        msg += f"Max open orders: {response.get('max_open_orders', 'Unknown')}\n"
        msg += f"Order value: {response.get('order_value', 'Unknown')}\n"
        msg += f"Leverage Long: {response.get('leverage_long', 'Unknown')}\n"
        msg += f"Leverage Short: {response.get('leverage_short', 'Unknown')}\n"
        msg += f"Active pairs: {', '.join(response.get('active_pairs', []))}\n\n"
        msg += f"Quantity of open trades: {response.get('open_trade_quantity', 'Unknown')}\n"
        msg += f"Open Trade Pairs: {', '.join(response.get('open_trade_pairs', []))} \n"
        msg += f"Current state: {response.get('current_state', 'Unknown')}\n"
        last_execution = response.get('last_execution', 'Unknown')
        if last_execution != 'Unknown':
            try:
                last_execution = datetime.fromisoformat(last_execution.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                telegram_logger.error(f"Error parsing last_execution datetime: {last_execution}")
                last_execution = 'Error'
        msg += f"Last execution (UTC): {last_execution}\n"
        msg += f"Current balance: USDT {response.get('balance', 'Unknown')}\n"

        update.message.reply_text(msg, parse_mode=ParseMode.HTML)

    except Exception as e:
        telegram_logger.error(f"Error getting status: {e}")
        update.message.reply_text("Error getting status", parse_mode=ParseMode.HTML)


def active_alerts(update, context):
    try:
        response = get_request("active_alerts")
        msg = "<b>Active Alerts:</b>\n\n"
        if not response:
            msg += "No active alerts."
        else:
            for alert in response:
                msg += f"Pair: {alert['pair']} Message: {alert['message']}\n\n"
        update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    except Exception as e:
        telegram_logger.error(f"Error getting active alerts: {e}")
        update.message.reply_text("Error getting active alerts", parse_mode=ParseMode.HTML)


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    telegram_logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TELEGRAM_API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("hard_reset", hard_reset))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("active_alerts", active_alerts))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    telegram_logger.info("Telegram Bot started")

    updater.idle()

if __name__ == "__main__":
    main()
