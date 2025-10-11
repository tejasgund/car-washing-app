import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Directory where log files will be stored
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Common log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with daily log rotation.
    Each module can import and use this.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if logger already configured
    if not logger.handlers:
        log_file = os.path.join(LOG_DIR, "app.log")
        handler = TimedRotatingFileHandler(
            log_file,
            when="midnight",   # Rotate logs every day at midnight
            interval=1,
            backupCount=7,     # Keep 7 days of logs
            encoding="utf-8"
        )
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
