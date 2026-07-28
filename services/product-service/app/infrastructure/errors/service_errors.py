class ServiceError(Exception):
    """Exceção base da aplicação."""
    pass

class DatabaseUnavailableError(ServiceError):
    pass

class ProductNotFoundError(ServiceError):
    pass


class ProductAlreadyExistsError(ServiceError):
    pass


class InvalidProductDataError(ServiceError):
    pass
    
class InsufficientStockError(ServiceError):
    pass
class AuthenticationError(ServiceError):
    pass
class InvalidTokenError(ServiceError):
    pass

class ExpiredTokenError(ServiceError):
    pass