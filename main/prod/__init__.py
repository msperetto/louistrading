import os
import logging
from config.config import LOG_LEVEL

# Configure logging
log_file_path = os.path.join(os.path.dirname(__file__), 'logs', 'trading_bot.log')
logging.basicConfig(
    filename=log_file_path,
    filemode='a',
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)