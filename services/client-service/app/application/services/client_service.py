from infrastructure.database.connection import DatabaseConnection
from infrastructure.repositories.client_repository import ClientRepository
from domain.entities.client import Client
from infrastructure.logger.logger import get_logger

logger = get_logger("ClientService")

class ClientService:
    def __init__(self):
        self.db = DatabaseConnection()
        self.repository = ClientRepository()
        
    def create_client(self, client: Client):
        with self.db.get_connection() as conn:
            try:
                logger.info(f"Iniciando criação do cliente: {client.email}")
                self.repository.save(client, conn)
                logger.info(f"Cliente inserido no Banco: {client.id}")
                
                conn.commit()
                logger.info(f"Transação finalizada com sucesso. {client.id}")
                return client  
            
            except Exception as e:
                conn.rollback()
                logger.error(f"Erro ao criar cliente: {client.id}")
                raise
            
    def get_client(self, client_id: str):
        with self.db.get_connection() as conn:
            try:
                logger.info(f"Buscando Cliente por ID: {client_id}")
                client = self.repository.get_by_id(client_id, conn)
                
                if not client:
                    logger.warning(f"Cliente não encontrado: {client_id}")
                    return None
                
                logger.info(f"Cliente encontrado: {client_id}")
                
                return client
            except Exception  as e:
                logger.error(f"Erro ao buscar cliente: {str(e)}")
                raise
        
    def get_all_clients(self):
        with self.db.get_connection() as conn:
            try:
                logger.info("Buscando clientes")
                
                clients = self.repository.get_all(conn)
                logger.info(f"{len(clients)} Clientes encontrados.")
                return clients
            
            except Exception as e:
                logger.error(f"Erro ao buscar os clientes: {str(e)}")
                raise
        
    def get_active_clients(self):
        with self.db.get_connection() as conn:
            try: 
                logger.info("Buscando clientes ativos")
                clients = self.repository.get_all_active(conn)
                logger.info(f"{len(clients)} Clientes ativos encontrados")
                return clients
            except Exception as e:
                logger.error(f"Erro ao buscar clientes ativos: {str(e)}")
                raise
            
        
    def get_inactive_clients(self):
        with self.db.get_connection() as conn:
            try:
                logger.info(f"Buscando todos os clientes inativos")
                clients = self.repository.get_all_inactive(conn)
                logger.info(f"{len(clients)} clientes inativos encontrados:")
                return clients
                
            except Exception as e:
                logger.error(f"Erro ao buscar clientes inativos: {str(e)}")
                raise
        
    def update_client(self, client: Client):
        with self.db.get_connection() as conn:
            try:
                logger.info(f"Iniciando a atualização do cliente: {client.id}")
                self.repository.update(client, conn)
                conn.commit()
                logger.info(f"Cliente atualizado com sucesso: {client.id}")
                
            except Exception as e:
                conn.rollback()
                logger.error(f"Erro ao atualizar cliente:{str(e)}")
                raise
            
    def delete_client(self, client_id: str):
        with self.db.get_connection() as conn:
            try:
                logger.info(f"Iniciando a desativação do cliente: {client_id}")
                self.repository.delete(client_id, conn)
                
                conn.commit()
                logger.warning(f"Cliente desativação com sucesso: {client_id}")
                
            except Exception as e :
                conn.rollback()
                logger.error(f"Erro ao desativar cliente: {str(e)}")
                raise
            
        
        
        
    