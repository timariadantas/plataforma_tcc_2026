import pytest
from unittest.mock import patch

from main import app

from infrastructure.errors.service_errors import (
    AuthenticationError,
    DatabaseUnavailableError
)

@pytest.fixture
def client():
    app.config["TESTING"] = True
    
    with app.test_client() as client:
        yield client
        
def test_login_successfully(client):
    with patch(
        "api.controller.auth_controller.auth_service.login"
    ) as login_mock:
        login_mock.return_value = "fake-jwt-token"
        
        response = client.post(
            "/auth/login",
            json={
                "email": "test@email.com",
                "password": "112233"
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data["token"] == "fake-jwt-token"
        
def test_return_401_when_credentials_are_invalid(client):

    with patch(
        "api.controller.auth_controller.auth_service.login"
    ) as login_mock:

        login_mock.side_effect = AuthenticationError(
            "Invalid email or password"
        )

        response = client.post(
            "/auth/login",
            json={
                "email": "maria@email.com",
                "password": "senhaerrada"
            }
        )

        assert response.status_code == 401

        data = response.get_json()

        assert data["error"] == "Invalid email or password"


def test_return_500_when_database_is_unavailable(client):

    with patch(
        "api.controller.auth_controller.auth_service.login"
    ) as login_mock:

        login_mock.side_effect = DatabaseUnavailableError(
            "Database unavailable"
        )

        response = client.post(
            "/auth/login",
            json={
                "email": "maria@email.com",
                "password": "123456"
            }
        )

        assert response.status_code == 500

        data = response.get_json()

        assert data["error"] == "Database unavailable"