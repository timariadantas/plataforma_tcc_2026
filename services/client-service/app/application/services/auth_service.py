from infrastructure.errors.service_errors import  AuthenticationError;
from infrastructure.security.jwt_handler import JwtHandler
from domain.repositories.client_repository_interface import ClientRepositoryInterface
import bcrypt


class AuthService:
    def __init__(self, client_repository: ClientRepositoryInterface):
       
        self.repository = client_repository
        self.jwt = JwtHandler()
        
    def login(self, email, password):
        user = self.repository.get_by_email(email)
        
        
        if not user:
            raise AuthenticationError("Invalid email or password")
        if not user.password_hash:
            raise AuthenticationError("Invalid email or password")
        
        stored_hash = user.password_hash
        if not bcrypt.checkpw(
            password.encode(),
            stored_hash.encode()
        ):
            raise  AuthenticationError("Invalid email or password")
        
        
        return self.jwt.generate_token({
            "client_id": user.id,
            "email" : user.email
        })
            
            
        
        