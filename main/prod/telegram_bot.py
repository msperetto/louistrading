import logging
import requests
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
from dotenv import load_dotenv
import os

# Get secret from file in production, environment variable in development
def _get_secret(secret_name):
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as secret_file:
            return secret_file.read().strip()
    except IOError:
        return None

load_dotenv()  # Ensure environment variables are loaded
TELEGRAM_API_KEY = _get_secret('telegram_api_key') or os.getenv("TELEGRAM_API_KEY")
BASE_URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_API_KEY)
BASE_LOCAL_URL = f"http://localhost:8000/"
MAX_MESSAGE_LEN = 4096

logger = logging.getLogger(__name__)

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
        logger.error(f"Error starting the bot: {e}")
        update.message.reply_text("Error starting the bot", parse_mode=ParseMode.HTML)


def stop(update, context):
    try:
        response = post_request("stop")
        # Check if response contains status key
        message = response.get('status', 'Unknown response')
        update.message.reply_text(message, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error stopping the bot: {e}")
        update.message.reply_text("Error stopping the bot", parse_mode=ParseMode.HTML)


def help(update, context):
    msg = "<b>Available commands:</b>\n\n"
    msg += "/start - Start the bot\n"
    msg += "/stop - Stop the bot\n"
    msg += "/help - Show this help message\n"
    update.message.reply_text(msg, parse_mode=ParseMode.HTML)


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TELEGRAM_API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info("Telegram Bot started")

    updater.idle()

if __name__ == "__main__":
    main()
