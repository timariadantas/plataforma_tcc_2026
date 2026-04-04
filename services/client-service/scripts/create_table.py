import sys
import os

# Permite importar o connection corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.database.connection import get_connection

def create_table():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        #  Dropa a tabela se já existir (evita erro)
        try:
            cursor.execute("DROP TABLE client")
            print(" Tabela antiga removida.")
        except:
            print(" Seguindo criação...")

        
        cursor.execute("""
        CREATE TABLE client (
            id VARCHAR2(36) PRIMARY KEY,
            name VARCHAR2(100) NOT NULL,
            surname VARCHAR2(100) NOT NULL,
            email VARCHAR2(150) NOT NULL,
            birthdate DATE NOT NULL,
            active NUMBER(1) DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        print("Tabela 'client' criada com sucesso!")

    except Exception as e:
        print(" Erro ao criar tabela:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_table()