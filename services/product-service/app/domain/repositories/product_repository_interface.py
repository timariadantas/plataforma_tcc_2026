
from abc import ABC, abstractmethod

class ProductRepositoryInterface(ABC):

    @abstractmethod
    def save(self, product):
        pass

    @abstractmethod
    def find_by_id(self, product_id):
        pass
    
    @abstractmethod
    def find_all(self,page=1, limit=10):
        pass

    @abstractmethod
    def update(self, product_id, data):
        pass

    @abstractmethod
    def delete(self, product_id):
        pass

    @abstractmethod
    def decrease_stock(self, product_id, quantity):
        pass