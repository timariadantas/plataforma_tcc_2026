class ServiceError(Exception):
    pass

class ValidationError(ServiceError):
    pass

class DatabaseUnavailableError(ServiceError):
    pass

class ClientNotFoundError(ServiceError):
    pass

class AuthenticationError(Exception):
    pass
