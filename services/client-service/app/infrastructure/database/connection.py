import os
import oracledb
from contextlib import contextmanager
from dotenv import load_dotenv
from infrastructure.logger.logger import get_logger

# Apenas para ambiente local (fora do Docker)
load_dotenv()

logger = get_logger("DatabaseConnection")


class DatabaseConnection:

    def __init__(self):
        self.user = os.getenv("CLIENT_DB_USER")
        self.password = os.getenv("CLIENT_DB_PASSWORD")
        self.host = os.getenv("CLIENT_DB_HOST")
        self.port = os.getenv("CLIENT_DB_PORT")
        self.service_name = os.getenv("CLIENT_DB_SERVICE")

        logger.info("Carregando variáveis de ambiente...")

        if not all([self.user, self.password, self.host, self.port, self.service_name]):
            logger.error("Variáveis de ambiente não configuradas corretamente")
            raise ValueError("Erro de configuração: verifique as variáveis de ambiente")

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
            logger.error(f"Erro ao conectar ou executar operação: {str(e)}")

            if conn:
                conn.rollback()

            raise

        finally:
            if conn:
                conn.close()