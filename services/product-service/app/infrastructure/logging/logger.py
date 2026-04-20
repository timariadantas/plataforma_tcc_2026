import logging
import queue
from logging.handlers import QueueHandler, QueueListener

#fila de logs
log_queue = queue.Queue()

# handler que escreve no console
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# handler que joga log na fila
queue_handler = QueueHandler(log_queue)

# logger principal
logger = logging.getLogger("product-service")
logger.setLevel(logging.INFO)
logger.addHandler(queue_handler)

#listener que consome a fila
listener = QueueListener(log_queue, console_handler)
listener.start()