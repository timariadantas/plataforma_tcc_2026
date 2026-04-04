import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.database.connection import DatabaseConnection


def create_table():
    db = DatabaseConnection()

    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()

            # Drop seguro
            try:
                cursor.execute("DROP TABLE client")
                print("Tabela antiga removida.")
            except Exception as e:
                if "ORA-00942" in str(e):
                    print("Tabela não existia, seguindo criação...")
                else:
                    raise

            # Create table
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
        print(f"Erro ao criar tabela: {e}")


if __name__ == "__main__":
    create_table()