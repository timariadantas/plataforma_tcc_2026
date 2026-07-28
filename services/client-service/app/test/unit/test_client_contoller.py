import pytest
from unittest.mock import patch, Mock

from main import app

from domain.entities.client import Client
from infrastructure.errors.service_errors import (
    ClientNotFoundError,
    DatabaseUnavailableError
)
from infrastructure.security.jwt_handler import JwtHandler

from datetime import date


@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client



@pytest.fixture
def token():

    
    return JwtHandler.generate_token(
        {
            "client_id": "123",
            "email": "teste@email.com"
        }
    )



def test_get_client_success(client, token):

    fake_client = Client(
        "Maria",
        "Dantas",
        "maria@email.com",
        "123456",
        date(1995,1,1)
    )

    fake_client.id = "1"


    with patch(
        "api.controller.client_controller.client_service"
    ) as mock_service:


        mock_service.get_client.return_value = fake_client


        response = client.get(
            "/clients/1",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )


        assert response.status_code == 200



def test_get_client_not_found(client, token):

    with patch(
        "api.controller.client_controller.client_service"
    ) as mock_service:


        mock_service.get_client.side_effect = ClientNotFoundError(
            "Client not found"
        )


        response = client.get(
            "/clients/1",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )


        assert response.status_code == 404



def test_get_client_without_token(client):


    response = client.get(
        "/clients/1"
    )


    assert response.status_code == 401



def test_get_all_clients(client, token):

    fake_client = Client(
        "Maria",
        "Dantas",
        "maria@email.com",
        "123456",
        date(1995,1,1)
    )


    with patch(
        "api.controller.client_controller.client_service"
    ) as mock_service:


        mock_service.get_all_clients.return_value = [
            fake_client
        ]


        response = client.get(
            "/clients",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )


        assert response.status_code == 200


        data = response.get_json()

        assert len(data) == 1



def test_get_all_clients_database_error(client, token):


    with patch(
        "api.controller.client_controller.client_service"
    ) as mock_service:


        mock_service.get_all_clients.side_effect = DatabaseUnavailableError(
            "Database unavailable"
        )


        response = client.get(
            "/clients",
            headers={
                "Authorization":f"Bearer {token}"
            }
        )


        assert response.status_code == 503