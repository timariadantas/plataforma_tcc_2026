import pytest
from unittest.mock import patch

from main import app

from domain.entities.client import Client

from infrastructure.errors.service_errors import (
    ClientNotFoundError,
    DatabaseUnavailableError,
    ClientEmailAlreadyExistsError
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


def assert_error_response(response, status_code, error_message):

    assert response.status_code == status_code

    data = response.get_json()

    assert data["message"] == "Request failed"
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["elapsed"], int)

    assert data["error"] == error_message

    assert "data" not in data


def assert_success_response(data):

    assert isinstance(data["message"], str)
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["elapsed"], int)

    assert "error" not in data


def test_get_client_success(client, token):

    client_mock = Client(
        id="123",
        name="Maria",
        surname="Dantas",
        email="maria@email.com",
        password_hash="secret",
        birthdate=date(1995, 5, 20),
        active=True
    )

    with patch(
        "api.controller.client_controller.client_service.get_client"
    ) as get_client_mock:

        get_client_mock.return_value = client_mock

        response = client.get(
            "/clients/123",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
    
        assert response.status_code == 200

        data = response.get_json()

        assert_success_response(data)

        client_data = data["data"]

        assert client_data["id"] == "123"
        assert client_data["name"] == "Maria"
        assert client_data["surname"] == "Dantas"
        assert client_data["email"] == "maria@email.com"
        assert client_data["birthdate"] == "1995-05-20"
        assert client_data["active"] is True

        assert "password" not in client_data
        assert "password_hash" not in client_data


def test_get_client_not_found(client, token):

    with patch(
        "api.controller.client_controller.client_service.get_client"
    ) as get_client_mock:

        get_client_mock.side_effect = ClientNotFoundError(
            "Client not found"
        )

        response = client.get(
            "/clients/123",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert_error_response(
            response,
            404,
            "Client not found"
        )


def test_get_client_without_token(client):

    response = client.get("/clients/123")

    assert_error_response(
        response,
        401,
        "Authentication required"
    )


def test_get_all_clients_database_error(client, token):

    with patch(
        "api.controller.client_controller.client_service.get_all_clients"
    ) as get_all_clients_mock:

        get_all_clients_mock.side_effect = DatabaseUnavailableError(
            "Database unavailable"
        )

        response = client.get(
            "/clients",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert_error_response(
            response,
            503,
            "Database unavailable"
        )


def test_create_client_success(client):

    created_client = Client(
        id="123",
        name="Maria",
        surname="Dantas",
        email="maria@email.com",
        password_hash="secret",
        birthdate=date(1995, 5, 20),
        active=True
    )

    with patch(
        "api.controller.client_controller.client_service.create_client"
    ) as create_client_mock:

        create_client_mock.return_value = created_client

        response = client.post(
            "/clients",
            json={
                "name": "Maria",
                "surname": "Dantas",
                "email": "maria@email.com",
                "password": "123456",
                "birthdate": "1995-05-20"
            }
        )

        assert response.status_code == 201

        data = response.get_json()

        assert_success_response(data)

        client_data = data["data"]

        assert client_data["id"] == "123"
        assert client_data["name"] == "Maria"
        assert client_data["surname"] == "Dantas"
        assert client_data["email"] == "maria@email.com"
        assert client_data["birthdate"] == "1995-05-20"
        assert client_data["active"] is True

        assert "password" not in client_data
        assert "password_hash" not in client_data


def test_create_client_invalid_data(client):

    response = client.post(
        "/clients",
        json={
            "name": "Maria",
            "surname": "Dantas",
            "password": "123456",
            "birthdate": "1995-05-20"
        }
    )

    data = response.get_json()

    assert response.status_code == 400

    assert data["message"] == "Request failed"
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["elapsed"], int)

    assert data["error"] == "email is required"

    assert "data" not in data


def test_create_client_email_already_exists(client):

    with patch(
        "api.controller.client_controller.client_service.create_client"
    ) as create_client_mock:

        create_client_mock.side_effect = ClientEmailAlreadyExistsError(
            "Email already exists"
        )

        response = client.post(
            "/clients",
            json={
                "name": "Maria",
                "surname": "Dantas",
                "email": "maria@email.com",
                "password": "123456",
                "birthdate": "1995-05-20"
            }
        )

        assert_error_response(
            response,
            409,
            "Email already exists"
        )


def test_update_client_success(client, token):

    updated_client = Client(
        id="123",
        name="Maria Updated",
        surname="Dantas",
        email="maria.updated@email.com",
        password_hash="secret",
        birthdate=date(1995, 5, 20),
        active=True
    )

    with patch(
        "api.controller.client_controller.client_service.update_client"
    ) as update_client_mock:

        update_client_mock.return_value = updated_client

        response = client.put(
            "/clients/123",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "name": "Maria Updated",
                "surname": "Dantas",
                "email": "maria.updated@email.com"
            }
        )

        assert response.status_code == 200

        data = response.get_json()

        assert_success_response(data)

        client_data = data["data"]

        assert client_data["id"] == "123"
        assert client_data["name"] == "Maria Updated"
        assert client_data["surname"] == "Dantas"
        assert client_data["email"] == "maria.updated@email.com"

        assert "password" not in client_data
        assert "password_hash" not in client_data


def test_update_client_invalid_data(client, token):

    response = client.put(
        "/clients/123",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Maria"
        }
    )

    data = response.get_json()

    assert response.status_code == 400

    assert data["message"] == "Request failed"
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["elapsed"], int)

    assert "error" in data
    assert "data" not in data


def test_update_client_not_found(client, token):

    with patch(
        "api.controller.client_controller.client_service.update_client"
    ) as update_client_mock:

        update_client_mock.side_effect = ClientNotFoundError(
            "Client not found"
        )

        response = client.put(
            "/clients/123",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "name": "Maria",
                "surname": "Dantas",
                "email": "maria@email.com"
            }
        )

        assert_error_response(
            response,
            404,
            "Client not found"
        )


def test_update_client_email_already_exists(client, token):

    with patch(
        "api.controller.client_controller.client_service.update_client"
    ) as update_client_mock:

        update_client_mock.side_effect = ClientEmailAlreadyExistsError(
            "Email already exists"
        )

        response = client.put(
            "/clients/123",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "name": "Maria",
                "surname": "Dantas",
                "email": "maria@email.com"
            }
        )

        assert_error_response(
            response,
            409,
            "Email already exists"
        )


def test_change_password_success(client, token):

    with patch(
        "api.controller.client_controller.client_service.change_password"
    ) as change_password_mock:

        response = client.patch(
            "/clients/123/password",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "new_password": "NovaSenha123"
            }
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["message"] == "Password updated successfully"
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["elapsed"], int)

        assert "data" not in data
        assert "error" not in data

        change_password_mock.assert_called_once()


def test_change_password_invalid_data(client, token):

    response = client.patch(
        "/clients/123/password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={}
    )

    data = response.get_json()

    assert response.status_code == 400

    assert data["message"] == "Request failed"
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["elapsed"], int)

    assert "error" in data
    assert "data" not in data


def test_change_password_not_found(client, token):

    with patch(
        "api.controller.client_controller.client_service.change_password"
    ) as change_password_mock:

        change_password_mock.side_effect = ClientNotFoundError(
            "Client not found"
        )

        response = client.patch(
            "/clients/123/password",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "new_password": "NovaSenha123"
            }
        )

        assert_error_response(
            response,
            404,
            "Client not found"
        )


def test_delete_client_success(client, token):

    with patch(
        "api.controller.client_controller.client_service.delete_client"
    ) as delete_client_mock:

        response = client.delete(
            "/clients/123",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 200

        data = response.get_json()

        assert data["message"] == "Client deactivated successfully"
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["elapsed"], int)

        assert "data" not in data
        assert "error" not in data

        delete_client_mock.assert_called_once_with("123")


def test_delete_client_not_found(client, token):

    with patch(
        "api.controller.client_controller.client_service.delete_client"
    ) as delete_client_mock:

        delete_client_mock.side_effect = ClientNotFoundError(
            "Client not found"
        )

        response = client.delete(
            "/clients/123",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert_error_response(
            response,
            404,
            "Client not found"
        )


def test_get_client_internal_server_error(client, token):

    with patch(
        "api.controller.client_controller.client_service.get_client"
    ) as get_client_mock:

        get_client_mock.side_effect = Exception(
            "Unexpected error"
        )

        response = client.get(
            "/clients/123",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert_error_response(
            response,
            500,
            "Internal server error"
        )

