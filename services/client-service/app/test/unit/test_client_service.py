import pytest
from unittest.mock import Mock
from datetime import date

from application.services.client_service import ClientService
from domain.entities.client import Client
from infrastructure.errors.service_errors import (
    ClientNotFoundError,
    DatabaseUnavailableError
)

@pytest.fixture
def repository_mock():
    return Mock()

@pytest.fixture
def service(repository_mock):
    return ClientService(repository_mock)


def create_client():
    return Client(
        name="Maria",
        surname="Dantas",
        email="maria@email.com",
        password_hash="123456",
        birthdate=date(2000,1,1)
    )


def test_create_client_success(service, repository_mock):
    client = create_client()

    result = service.create_client(client)

    repository_mock.save.assert_called_once_with(client)

    assert result == client
    assert result.password_hash != "123456"


def test_get_client_success(service, repository_mock):
    client = create_client()

    repository_mock.get_by_id.return_value = client

    result = service.get_client("123")

    repository_mock.get_by_id.assert_called_once_with("123")

    assert result == client


def test_get_client_not_found(service, repository_mock):

    repository_mock.get_by_id.return_value = None

    with pytest.raises(ClientNotFoundError):

        service.get_client("999")


def test_get_all_clients(service, repository_mock):

    repository_mock.get_all.return_value = []

    result = service.get_all_clients()

    repository_mock.get_all.assert_called_once()

    assert result == []


def test_get_active_clients(service, repository_mock):

    repository_mock.get_all_active.return_value = []

    result = service.get_active_clients()

    assert result == []


def test_get_inactive_clients(service, repository_mock):

    repository_mock.get_all_inactive.return_value = []

    result = service.get_inactive_clients()

    assert result == []

def test_update_client(service, repository_mock):

    client = create_client()

    result = service.update_client(client)

    repository_mock.update.assert_called_once_with(client)

    assert result == client

def test_change_password(service, repository_mock):
    service.change_password(
        "123",
        "novaSenha123"
    )

    repository_mock.update_password.assert_called_once()


def test_delete_client(service, repository_mock):

    service.delete_client("123")

    repository_mock.delete.assert_called_once_with("123")



def test_create_client_database_error(service, repository_mock):

    repository_mock.save.side_effect = Exception("Database down")


    client = create_client()


    with pytest.raises(DatabaseUnavailableError):

        service.create_client(client)