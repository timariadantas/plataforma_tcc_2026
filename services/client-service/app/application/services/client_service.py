from domain.entities.client import Client
from infrastructure.logger.logger import get_logger
from infrastructure.errors.service_errors import (
    DatabaseUnavailableError, 
    ClientNotFoundError, 
    ClientEmailAlreadyExistsError
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

            return client

        except ClientEmailAlreadyExistsError:
            raise

        except DatabaseUnavailableError:
            raise

        except Exception as e:
            logger.error(f"Unexpected error creating client: {str(e)}")
            raise DatabaseUnavailableError(
                "Client service temporarily unavailable"
            ) from e

  
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
        except DatabaseUnavailableError:
            raise

        except Exception as e:
            logger.error(f"Unexpected database error fetching client: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e

   
    def get_all_clients(self):
        try:
            return self.repository.get_all()
        
        except DatabaseUnavailableError:
            raise

        except Exception as e:
            logger.error(f"Unexpected database error fetching clients: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e


    def get_active_clients(self):
        try:
            return self.repository.get_all_active()
        
        except DatabaseUnavailableError:
            raise

        except Exception as e:
            logger.error(f"Unexpected database error fetching active clients: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e


    def get_inactive_clients(self):  
        try:
            return self.repository.get_all_inactive()
        
        except DatabaseUnavailableError:
            raise
        
        except Exception as e:
            logger.error(f"Unexpected database error fetching inactive clients: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e

    def update_client(
    self,
    client_id: str,
    name: str,
    surname: str,
    email: str
):
        try:
            logger.info(f"Updating client: {client_id}")

            self.repository.update(
                client_id=client_id,
                name=name,
                surname=surname,
                email=email
        )

            logger.info(f"Client updated: {client_id}")

            return self.repository.get_by_id(client_id)

        except ClientNotFoundError:
            raise

        except ClientEmailAlreadyExistsError:
            raise

        except DatabaseUnavailableError:
            raise

        except Exception as e:
            logger.error(f"Unexpected error updating client: {str(e)}")

        raise DatabaseUnavailableError(
            "Client service temporarily unavailable"
        ) from e
   
    def change_password(self, client_id, new_password):
        try:
            logger.info(f"Changing password for client: {client_id}")

            hashed = bcrypt.hashpw(
            new_password.encode(),
            bcrypt.gensalt()
            ).decode()

            self.repository.update_password(client_id, hashed)

            logger.info(f"Password updated: {client_id}")

        except ClientNotFoundError:
            raise

        except DatabaseUnavailableError:
            raise
        
        except Exception as e:
            logger.error(f"Unexpected database error changing password:{str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e
    
    def delete_client(self, client_id: str):
        try:
            logger.info(f"Deleting client: {client_id}")

            self.repository.delete(client_id)

            logger.warning(f"Client deleted: {client_id}")
            
        except ClientNotFoundError:
            raise

        except DatabaseUnavailableError:
            raise
        
        except Exception as e:
            logger.error(f"Unexpected database error deleting client: {str(e)}")
            raise DatabaseUnavailableError("Client service temporarily unavailable") from e