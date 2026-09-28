class ServiceError(Exception):
    """Base exception for application errors."""
    pass


class ValidationError(ServiceError): #400
    """Invalid data supplied by the client."""
    pass


class DatabaseUnavailableError(ServiceError): #503
    """Database or required infrastructure is unavailable."""
    pass


class ClientNotFoundError(ServiceError): #404
    """Requested client does not exist."""
    pass


class ClientEmailAlreadyExistsError(ServiceError): #409
    """Client email is already registered."""
    pass


class AuthenticationError(ServiceError): #401
    """Authentication failed."""
    pass

