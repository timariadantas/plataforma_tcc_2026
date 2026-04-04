from venv import logger

from dotenv import load_dotenv
load_dotenv()

import os
import oracledb
from contextlib import contextmanager
from infrastructure.logger.logger import get_logger

logger = get_logger("DatabaseConnection")


class DatabaseConnection:

    def __init__(self):
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.service_name = os.getenv("DB_SERVICE")
        
        if not all([self.user, self.password, self.host, self.port, self.service_name]):
            logger.error("Variáveis de ambiente não configuradas corretamente")
            raise Exception("Erro de configuração: verifique o arquivo .env")

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            dsn = oracledb.makedsn(
                self.host,
                self.port,
                service_name=self.service_name
            )

            conn = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=dsn
            )

            yield conn
            

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Erro ao conectar ou executar operação: {str(e)}")
            raise

        finally:
            if conn:
                conn.close()