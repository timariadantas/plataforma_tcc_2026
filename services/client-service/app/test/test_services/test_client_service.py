import pytest
from datetime import date, datetime

from application.services.client_service import ClientService
from domain.entities.client import Client


@pytest.fixture
def service():
    return ClientService()


def test_create_client(service):
    client = Client(
        name="Maria",
        surname="Dantas",
        email=f"maria_{datetime.now().timestamp()}@test.com",
        birthdate=date(1990, 1, 1)
    )

    result = service.create_client(client)

    assert result is not None
    assert result.id is not None
    assert result.name == "Maria"
    assert result.email == client.email
    assert result.active is True



def test_get_client(service):
    client = Client(
        name="João",
        surname="Silva",
        email=f"joao_{datetime.now().timestamp()}@test.com",
        birthdate=date(1995, 5, 5)
    )

    created = service.create_client(client)

    found = service.get_client(created.id)

    assert found is not None
    assert found.id == created.id
    assert found.email == client.email


def test_update_client(service):
    client = Client(
        name="Carlos",
        surname="Souza",
        email=f"carlos_{datetime.now().timestamp()}@test.com",
        birthdate=date(1980, 3, 10)
    )

    created = service.create_client(client)

    created.name = "Carlos Atualizado"
    created.email = "carlos_updated@test.com"

    updated = service.update_client(created)

    assert updated.name == "Carlos Atualizado"
    assert updated.email == "carlos_updated@test.com"



def test_delete_client(service):
    client = Client(
        name="Ana",
        surname="Pereira",
        email=f"ana_{datetime.now().timestamp()}@test.com",
        birthdate=date(1992, 7, 20)
    )

    created = service.create_client(client)

    service.delete_client(created.id)

    result = service.get_client(created.id)

    assert result is None or result.active is False



def test_get_all_clients(service):
    result = service.get_all_clients()

    assert isinstance(result, list)



def test_get_active_clients(service):
    result = service.get_active_clients()

    assert isinstance(result, list)



def test_get_inactive_clients(service):
    result = service.get_inactive_clients()

    assert isinstance(result, list)