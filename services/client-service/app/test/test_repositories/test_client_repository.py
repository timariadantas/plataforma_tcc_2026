import pytest

from datetime import date, datetime
from domain.entities.client import Client
from infrastructure.database.connection import DatabaseConnection
from infrastructure.repositories.client_repository import ClientRepository

@pytest.fixture
def repo():
    db = DatabaseConnection()
    return ClientRepository(db)


def test_save_and_get_by_id(repo):
    client = Client(
        name="Maria",
        surname="Dantas",
        email=f"maria_{datetime.now().timestamp()}@test.com",
        birthdate=date(1990, 1, 1)
    )

    repo.save(client)

    result = repo.get_by_id(client.id)

    assert result is not None
    assert result.email == client.email
    assert result.name == "Maria"
    assert result.active is True


def test_update_client(repo):
    client = Client(
        name="João",
        surname="Silva",
        email=f"joao_{datetime.now().timestamp()}@test.com",
        birthdate=date(1995, 5, 5)
    )

    repo.save(client)

    client.name = "João Atualizado"
    client.email = "joao_updated@test.com"

    repo.update(client)

    updated = repo.get_by_id(client.id)

    assert updated.name == "João Atualizado"
    assert updated.email == "joao_updated@test.com"



def test_delete_client(repo):
    client = Client(
        name="Carlos",
        surname="Souza",
        email=f"carlos_{datetime.now().timestamp()}@test.com",
        birthdate=date(1980, 3, 10)
    )

    repo.save(client)

    repo.delete(client.id)

    result = repo.get_by_id(client.id)

    assert result.active is False



def test_get_all(repo):
    result = repo.get_all()

    assert isinstance(result, list)


def test_get_all_active(repo):
    result = repo.get_all_active()

    assert isinstance(result, list)


def test_get_all_inactive(repo):
    result = repo.get_all_inactive()

    assert isinstance(result, list)