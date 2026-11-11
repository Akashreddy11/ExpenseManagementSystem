import logging
from pathlib import Path

# Fix 1: Pin the log file path relative to this file's directory
# This ensures server.log is always written to the backend folder (or change to .parent.parent for root)
LOG_DIR = Path(__file__).resolve().parent
LOG_FILE = LOG_DIR / "server.log"


def getlogger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Fix 2: Only add the handler if this logger doesn't already have one
    # This prevents duplicate log lines during Streamlit re-runs
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        file_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    # Fix 3: Prevent log messages from getting swallowed or duplicated by Streamlit's root logger
    logger.propagate = False

    return logger