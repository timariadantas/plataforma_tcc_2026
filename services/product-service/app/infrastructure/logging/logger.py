import logging
import os

def get_logger(name: str):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger(name)

    
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger