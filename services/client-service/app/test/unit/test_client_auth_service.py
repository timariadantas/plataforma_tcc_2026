import bcrypt 
import pytest

from unittest.mock import Mock, patch

from application.services.auth_service import AuthService
from infrastructure.errors.service_errors import AuthenticationError

@pytest.fixture
def repository():
    return Mock()

@pytest.fixture
def service(repository):
    return AuthService(repository)

def test_login_successfuly(service, repository):
    
    password = "112233"

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()
    
    user = Mock()
    user.id = "123"
    user.email = "test@email.com"
    user.password_hash = hashed
    
    repository.get_by_email.return_value = user
    
    with patch.object(
        service.jwt,
        "generate_token",
        return_value="fake-jwt"
    ) as jwt_mock:
        
        token = service.login(
            "test@email.com",
            password
        )
        
        assert token == "fake-jwt"
        
        jwt_mock.assert_called_once_with({
            "client_id" : "123",
            "email": "test@email.com"
        })
        
def test_raise_error_when_user_not_found(
    service,
    repository
):
    repository.get_by_email.return_value = None
    
    with pytest.raises(AuthenticationError):
        
        service.login(
            "test@email.com",
            "112233"
        )
        
def test_raise_error_when_password_hash_is_empty(
    service,
    repository
):
    user = Mock()
    user.password_hash = None
    
    repository.get_by_email.return_value = user
    
    with pytest.raises(AuthenticationError):
        service.login(
            "test@email.com",
            "112233"
        )
        
def test_raise_error_when_password_is_invalid(
    service,
    repository
):
    hashed = bcrypt.hashpw(
        "445566".encode(),
        bcrypt.gensalt()
    ).decode()
    
    user = Mock()
    
    user.id = "123"
    user.email = "test@email.com"
    user.password_hash = hashed
    
    repository.get_by_email.return_value = user
    
    with pytest.raises(AuthenticationError):
        service.login(
            "test@email.com",
            "112233"
        )