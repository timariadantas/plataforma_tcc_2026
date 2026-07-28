from abc import ABC, abstractmethod

class ClientRepositoryInterface(ABC):
    @abstractmethod
    def save(self, client):
        pass
    
    @abstractmethod
    def get_by_id(self, client_id):
        pass
    
    @abstractmethod
    def update(self, client):
        pass
    
    @abstractmethod
    def get_all(self):
        pass 
    
    @abstractmethod
    def get_all_active(self):
        pass
    
    @abstractmethod
    def get_all_inactive(self):
        pass
    @abstractmethod
    def update_password(self, client_id:str, password_hash:str):
        pass
    @abstractmethod
    def delete(self, client_id):
        pass
    
    @abstractmethod
    def get_by_email(self, email:str):
        pass
    