from abc import ABC, abstractmethod

class ProductRepositoryInterface(ABC):
    
    @abstractmethod
    def save(self, product):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, product_id):
        pass

    @abstractmethod
    def update(self, product_id, data):
        pass

    @abstractmethod
    def delete(self, product_id):
        pass
