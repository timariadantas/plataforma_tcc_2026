import logging
import logging.handlers
import os
from queue import Queue

log_queue = Queue()

def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    listener = logging.handlers.QueueListener(
        log_queue,
        file_handler,
        console_handler
    )
    
    listener.start()
    return listener


def get_logger(name: str):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
    
        queue_handler = logging.handlers.QueueHandler(log_queue)
        logger.addHandler(queue_handler)
    
    return logger