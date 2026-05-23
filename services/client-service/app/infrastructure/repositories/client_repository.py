from domain.repositories.client_repository_interface import ClientRepositoryInterface
from domain.entities.client import Client
from datetime import datetime, timezone
from infrastructure.logger.logger import get_logger

logger = get_logger("ClientRepository")


class ClientRepository(ClientRepositoryInterface):

    def __init__(self, db_connection):
        self.db = db_connection
        
    def save(self, client: Client):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                logger.info(f"Inserting client: {client.email}")

                cursor.execute("""
                    INSERT INTO client (
                        id, name, surname, email, birthdate,
                        active, created_at, updated_at
                    ) VALUES (
                        :id, :name, :surname, :email, :birthdate,
                        :active, :created_at, :updated_at
                    )
                """, {
                    "id": client.id,
                    "name": client.name,
                    "surname": client.surname,
                    "email": client.email,
                    "birthdate": client.birthdate,
                    "active": 1 if client.active else 0,
                    "created_at": client.created_at,
                    "updated_at": client.updated_at
                })

                conn.commit()
                logger.info(f"Client inserted successfully: {client.id}")

            except Exception as e:
                conn.rollback()
                logger.error(f"Error inserting client: {str(e)}")
                raise
            finally:
                cursor.close()

   
    def get_by_id(self, client_id: str):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                logger.info(f"Fetching client by ID: {client_id}")

                cursor.execute("""
                    SELECT id, name, surname, email, birthdate, active,
                           created_at, updated_at
                    FROM client
                    WHERE id = :id
                """, {"id": client_id})

                row = cursor.fetchone()

                if not row:
                    logger.warning(f"Client not found: {client_id}")
                    return None

                return self._map_to_entity(row)

            except Exception as e:
                logger.error(f"Error fetching client: {str(e)}")
                raise
            finally:
                cursor.close()

 
    def get_all(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                logger.info("Fetching all clients")

                cursor.execute("""
                    SELECT id, name, surname, email, birthdate, active,
                           created_at, updated_at
                    FROM client
                """)

                rows = cursor.fetchall()

                return [self._map_to_entity(row) for row in rows]

            except Exception as e:
                logger.error(f"Error fetching all clients: {str(e)}")
                raise
            finally:
                cursor.close()

   
    def get_all_active(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                logger.info("Fetching active clients")

                cursor.execute("""
                    SELECT id, name, surname, email, birthdate, active,
                           created_at, updated_at
                    FROM client
                    WHERE active = 1
                """)

                rows = cursor.fetchall()
                return [self._map_to_entity(row) for row in rows]

            except Exception as e:
                logger.error(f"Error fetching active clients: {str(e)}")
                raise
            finally:
                cursor.close()

   
    def get_all_inactive(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                logger.info("Fetching inactive clients")

                cursor.execute("""
                    SELECT id, name, surname, email, birthdate, active,
                           created_at, updated_at
                    FROM client
                    WHERE active = 0
                """)

                rows = cursor.fetchall()
                return [self._map_to_entity(row) for row in rows]

            except Exception as e:
                logger.error(f"Error fetching inactive clients: {str(e)}")
                raise
            finally:
                cursor.close()

   
    def update(self, client: Client):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                logger.info(f"Updating client: {client.id}")

                cursor.execute("""
                    UPDATE client
                    SET name = :name,
                        surname = :surname,
                        email = :email,
                        updated_at = :updated_at
                    WHERE id = :id
                """, {
                    "id": client.id,
                    "name": client.name,
                    "surname": client.surname,
                    "email": client.email,
                    "updated_at": datetime.now(timezone.utc)
                })

                conn.commit()
                logger.info(f"Client updated: {client.id}")

            except Exception as e:
                conn.rollback()
                logger.error(f"Error updating client: {str(e)}")
                raise
            finally:
                cursor.close()

   
    def delete(self, client_id: str):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                logger.info(f"Deactivating client: {client_id}")

                cursor.execute("""
                    UPDATE client
                    SET active = 0,
                        updated_at = :updated_at
                    WHERE id = :id
                """, {
                    "id": client_id,
                    "updated_at": datetime.now(timezone.utc)
                })

                conn.commit()
                logger.info(f"Client deactivated: {client_id}")

            except Exception as e:
                conn.rollback()
                logger.error(f"Error deleting client: {str(e)}")
                raise
            finally:
                cursor.close()

    
    # Mapper( banco para entitidade)
   
    def _map_to_entity(self, row):
        client = Client(
            name=row[1],
            surname=row[2],
            email=row[3],
            birthdate=row[4]
        )

        client.id = row[0]
        client.active = bool(row[5])
        client.created_at = row[6]
        client.updated_at = row[7]

        return client