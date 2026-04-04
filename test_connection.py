from dotenv import load_dotenv
load_dotenv()

import os
import oracledb

try:
    dsn = oracledb.makedsn(
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        service_name=os.getenv("DB_SERVICE")
    )

    connection = oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=dsn
    )

    print(" Conectado com sucesso!")

    connection.close()

except Exception as e:
    print(" Erro na conexão:", e)