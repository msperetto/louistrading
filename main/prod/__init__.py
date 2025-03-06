import os
import logging
from config.config import LOG_LEVEL

# Configure logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_path = os.path.join(log_dir, 'trading_bot.log')
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w'):
        pass

logging.basicConfig(
    filename=log_file_path,
    filemode='a',
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)