from domain.entities.client import Client
from infrastructure.logger.logger import get_logger
from infrastructure.errors.service_errors import (
    DatabaseUnavailableError, ClientNotFoundError
)
import bcrypt

logger = get_logger("ClientService")


class ClientService:

    def __init__(self, repository):
        
        self.repository = repository


    def create_client(self, client: Client):
        try:
            logger.info(f"Creating client: {client.email}")
            hashed = bcrypt.hashpw(
            client.password_hash.encode(),
            bcrypt.gensalt()
            ).decode()

            client.password_hash = hashed

            self.repository.save(client)

            logger.info(">>> HASHING PASSWORD ATUAL")
            return client

        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e

  
    def get_client(self, client_id: str):
        try:
            logger.info(f"Fetching client: {client_id}")

            client = self.repository.get_by_id(client_id)

            if not client:
                logger.warning(f"Client not found: {client_id}")
                raise ClientNotFoundError(f"Client {client_id} not found")

            return client
        except ClientNotFoundError:
            raise

        except Exception as e:
            logger.error(f"Database failure on get: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e

   
    def get_all_clients(self):
        try:
            return self.repository.get_all()

        except Exception as e:
            logger.error(f"Database failure on active {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e


    def get_active_clients(self):
        try:
            return self.repository.get_all_active()

        except Exception as e:
            logger.error(f"Database failure on active: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e


    def get_inactive_clients(self):  
        try:
            return self.repository.get_all_inactive()

        except Exception as e:
            logger.error(f"Database failure on active: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e

    
    def update_client(self, client: Client):
        try:
            logger.info(f"Updating client: {client.id}")

            self.repository.update(client)

            logger.info(f"Client updated: {client.id}")
            return client

        except Exception as e:
            logger.error(f"Database failure on update: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e

    def change_password(self, client_id, new_password):
        try:
            logger.info(f"Changing password for client: {client_id}")

            hashed = bcrypt.hashpw(
            new_password.encode(),
            bcrypt.gensalt()
            ).decode()

            self.repository.update_password(client_id, hashed)

            logger.info(f"Password updated: {client_id}")

        except Exception as e:
            logger.error(f"Error changing password: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e
    
    def delete_client(self, client_id: str):
        try:
            logger.info(f"Deleting client: {client_id}")

            self.repository.delete(client_id)

            logger.warning(f"Client deleted: {client_id}")

        except Exception as e:
            logger.error(f"Database failure on delete: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e