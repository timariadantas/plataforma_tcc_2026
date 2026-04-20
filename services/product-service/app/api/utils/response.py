import time
from datetime import datetime

def build_response(start_time, message, data=None, error=None):
    return {
        "mensagem": message,
        "timestamp": datetime.now().isoformat(),
        "decorrido": int((time.time() - start_time) * 1000),
        "data": data,
        "erro": error
    }