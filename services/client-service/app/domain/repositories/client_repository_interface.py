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
    def get_all_active(self, conn):
        pass
    
    @abstractmethod
    def get_all_inactive(self, conn):
        pass
    
    @abstractmethod
    def delete(self, client_id):
        pass
    