from infrastructure.database.connection import DatabaseConnection
from infrastructure.repositories.client_repository import ClientRepository
from domain.entities.client import Client
from infrastructure.logger.logger import get_logger

logger = get_logger("ClientService")


class ClientService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.repository = ClientRepository(self.db)


    def create_client(self, client: Client):
        try:
            logger.info(f"Creating client: {client.email}")

            self.repository.save(client)

            logger.info(f"Client created: {client.id}")
            return client

        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            raise

  
    def get_client(self, client_id: str):
        try:
            logger.info(f"Fetching client: {client_id}")

            client = self.repository.get_by_id(client_id)

            if not client:
                logger.warning(f"Client not found: {client_id}")
                return None

            return client

        except Exception as e:
            logger.error(f"Error fetching client: {str(e)}")
            raise

   
    def get_all_clients(self):
        try:
            return self.repository.get_all()

        except Exception as e:
            logger.error(f"Error fetching clients: {str(e)}")
            raise


    def get_active_clients(self):
        try:
            return self.repository.get_all_active()

        except Exception as e:
            logger.error(f"Error active clients: {str(e)}")
            raise


    def get_inactive_clients(self):
        try:
            return self.repository.get_all_inactive()

        except Exception as e:
            logger.error(f"Error inactive clients: {str(e)}")
            raise

    
    def update_client(self, client: Client):
        try:
            logger.info(f"Updating client: {client.id}")

            self.repository.update(client)

            logger.info(f"Client updated: {client.id}")
            return client

        except Exception as e:
            logger.error(f"Error updating client: {str(e)}")
            raise

    
    def delete_client(self, client_id: str):
        try:
            logger.info(f"Deleting client: {client_id}")

            self.repository.delete(client_id)

            logger.warning(f"Client deleted: {client_id}")

        except Exception as e:
            logger.error(f"Error deleting client: {str(e)}")
            raise