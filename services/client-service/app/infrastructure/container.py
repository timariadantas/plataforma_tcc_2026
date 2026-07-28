from infrastructure.database.connection import DatabaseConnection
from infrastructure.repositories.client_repository import ClientRepository
from application.services.auth_service import AuthService
from application.services.client_service import ClientService

# instância única de banco
db = DatabaseConnection()

client_repository = ClientRepository(db)

auth_service = AuthService(client_repository)
client_service = ClientService(client_repository)