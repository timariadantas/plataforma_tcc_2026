import json
from datetime import date
from unittest.mock import MagicMock

from domain.entities.client import Client
from main import app


def test_create_client_success(mocker):

    fake_service = MagicMock()

    mocker.patch(
        "api.controller.client_controller.service",
        fake_service
    )

    client = Client(
        name="Maria",
        surname="Dantas",
        email="maria@gmail.com",
        birthdate=date(1990, 1, 1)
    )

    fake_service.create_client.return_value = client

    client_app = app.test_client()

    response = client_app.post(
        "/clients",
        data=json.dumps({
            "name": "Maria",
            "surname": "Dantas",
            "email": "maria@gmail.com",
            "birthdate": "1990-01-01"
        }),
        content_type="application/json"
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Maria"
    assert data["surname"] == "Dantas"
    assert data["email"] == "maria@gmail.com"


def test_get_client_success(mocker):

    fake_service = MagicMock()

    mocker.patch(
        "api.controller.client_controller.service",
        fake_service
    )

    client = Client(
        name="Carlos",
        surname="Silva",
        email="carlos@gmail.com",
        birthdate=date(1995, 5, 10)
    )

    fake_service.get_client.return_value = client

    client_app = app.test_client()

    response = client_app.get(f"/clients/{client.id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["email"] == "carlos@gmail.com"


def test_get_client_not_found(mocker):

    fake_service = MagicMock()

    mocker.patch(
        "api.controller.client_controller.service",
        fake_service
    )

    fake_service.get_client.return_value = None

    client_app = app.test_client()

    response = client_app.get("/clients/123")

    assert response.status_code == 404

    data = response.get_json()

    assert data["message"] == "Client not found"


def test_get_all_clients(mocker):

    fake_service = MagicMock()

    mocker.patch(
        "api.controller.client_controller.service",
        fake_service
    )

    client1 = Client(
        name="Maria",
        surname="Dantas",
        email="maria@gmail.com",
        birthdate=date(1990, 1, 1)
    )

    client2 = Client(
        name="Carlos",
        surname="Silva",
        email="carlos@gmail.com",
        birthdate=date(1995, 5, 10)
    )

    fake_service.get_all_clients.return_value = [client1, client2]

    client_app = app.test_client()

    response = client_app.get("/clients")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2


def test_update_client_success(mocker):

    fake_service = MagicMock()

    mocker.patch(
        "api.controller.client_controller.service",
        fake_service
    )

    client_app = app.test_client()

    response = client_app.put(
        "/clients/123",
        data=json.dumps({
            "name": "Maria",
            "surname": "Silva",
            "email": "maria@gmail.com",
            "birthdate": "1990-01-01"
        }),
        content_type="application/json"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Client updated successfully"


def test_delete_client_success(mocker):

    fake_service = MagicMock()

    mocker.patch(
        "api.controller.client_controller.service",
        fake_service
    )

    client_app = app.test_client()

    response = client_app.delete("/clients/123")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Client disabled successfully"