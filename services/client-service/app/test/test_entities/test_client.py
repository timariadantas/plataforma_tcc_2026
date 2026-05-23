import pytest
from datetime import date
from domain.entities.client import Client


def test_create_client_success():
    birthdate = date(1990, 1, 1)

    client = Client(
        name="Maria",
        surname="Dantas",
        email="maria@gmail.com",
        birthdate=birthdate
    )

    assert client.name == "Maria"
    assert client.surname == "Dantas"
    assert client.email == "maria@gmail.com"
    assert client.active is True
    assert client.created_at is not None
    assert client.updated_at is not None


def test_client_update_success():
    birthdate = date(1990, 1, 1)

    client = Client(
        name="Leonardo",
        surname="Silva",
        email="leo@gmail.com",
        birthdate=birthdate
    )

    client.update("Severo", "Silva", "severo@gmail.com")

    assert client.name == "Severo"
    assert client.surname == "Silva"
    assert client.email == "severo@gmail.com"
    assert client.updated_at >= client.created_at


def test_client_disable():
    birthdate = date(1969, 7, 31)

    client = Client(
        name="Leonardo",
        surname="Silva",
        email="leo@gmail.com",
        birthdate=birthdate
    )

    client.disable()

    assert client.active is False
    assert client.updated_at >= client.created_at


def test_invalid_email_raises():
    birthdate = date(1969, 1, 2)

    with pytest.raises(ValueError, match="Email inválido"):
        Client(
            name="Leonardo",
            surname="Silva",
            email="leogmail.com",
            birthdate=birthdate
        )