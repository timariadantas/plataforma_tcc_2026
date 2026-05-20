from venv import logger

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[5] / ".env"
load_dotenv(env_path)

import os
import oracledb
from contextlib import contextmanager
from infrastructure.logger.logger import get_logger

logger = get_logger("DatabaseConnection")


class DatabaseConnection:

    def __init__(self):
        self.user = os.getenv("CLIENT_DB_USER")
        self.password = os.getenv("CLIENT_DB_PASSWORD")
        self.host = os.getenv("CLIENT_DB_HOST")
        self.port = os.getenv("CLIENT_DB_PORT")
        self.service_name = os.getenv("CLIENT_DB_SERVICE")
        
        print("CLIENT_DB_USER:", self.user)
        print("CLIENT_DB_PASSWORD:", self.password)
        print("CLIENT_DB_HOST:", self.host)
        print("CLIENT_DB_PORT:", self.port)
        print("CLIENT_DB_SERVICE:", self.service_name)
        
        if not all([self.user, self.password, self.host, self.port, self.service_name]):
            logger.error("Variáveis de ambiente não configuradas corretamente")
            raise ValueError("Erro de configuração: verifique o arquivo .env")

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