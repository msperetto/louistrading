import os
import logging
from logging.handlers import RotatingFileHandler
from config.config import LOG_LEVEL

def setup_logger(logger_name, log_file, level=LOG_LEVEL):
    """
    Setup a new logger with its own file handler
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create or get logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create file handler
    log_file_path = os.path.join(log_dir, log_file)
    handler = RotatingFileHandler(
        log_file_path,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handler to logger if it doesn't already have it
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

# Setup default trading bot logger
logger = setup_logger('trading_bot', 'trading_bot.log')

# Setup telegram bot logger
telegram_logger = setup_logger('telegram_bot', 'telegram.log')

# Setup telegram notification logger
telegram_notify_logger = setup_logger('telegram_notify', 'telegram_notify.log')

# Setup AWS logger
aws_logger = setup_logger('aws', 'aws.log')

# Setup API logger
api_logger = setup_logger('api', 'api.log')

# Setup Marlin Stop logger
marlin_stop_logger = setup_logger('marlin_stop', 'marlin_stop.log')

# Setup Stop Thread logger
stop_thread_logger = setup_logger('stop_thread', 'stop_thread.log')

# Setup Binance logger
binance_logger = setup_logger('binance', 'binance.log')

# Setup test logger
test_logger = setup_logger('test', 'test.log')

# Setup Notification object
from prod.notification import Notification
notify = Notification()

