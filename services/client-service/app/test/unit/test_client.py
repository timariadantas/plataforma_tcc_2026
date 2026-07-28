import pytest
from datetime import date
from domain.entities.client import Client
from infrastructure.errors.service_errors import ValidationError


def test_should_create_client():
    client = Client(
        name="Maria",
        surname="Dantas",
        email="maria@email.com",
        password_hash="123456",
        birthdate=date(2000, 1, 1)
    )

    assert client.name == "Maria"
    assert client.surname == "Dantas"
    assert client.email == "maria@email.com"
    assert client.password_hash == "123456"
    assert client.active is True
    assert client.id is not None
    assert client.created_at is not None
    assert client.updated_at is not None


def test_should_raise_validation_error_when_name_is_empty():
    with pytest.raises(ValidationError):
        Client(
            "",
            "Dantas",
            "maria@email.com",
            "123456",
            date(2000, 1, 1)
        )


def test_should_raise_validation_error_when_surname_is_empty():
    with pytest.raises(ValidationError):
        Client(
            "Maria",
            "",
            "maria@email.com",
            "123456",
            date(2000, 1, 1)
        )


def test_should_raise_validation_error_when_email_is_invalid():
    with pytest.raises(ValidationError):
        Client(
            "Maria",
            "Dantas",
            "emailinvalido",
            "123456",
            date(2000, 1, 1)
        )


def test_should_raise_validation_error_when_password_is_invalid():
    with pytest.raises(ValidationError):
        Client(
            "Maria",
            "Dantas",
            "maria@email.com",
            "123",
            date(2000, 1, 1)
        )


def test_should_raise_validation_error_when_birthdate_is_invalid():
    with pytest.raises(ValidationError):
        Client(
            "Maria",
            "Dantas",
            "maria@email.com",
            "123456",
            "01/01/2000"
        )


def test_should_update_client():
    client = Client(
        "Maria",
        "Dantas",
        "maria@email.com",
        "123456",
        date(2000, 1, 1)
    )
    created_at = client.created_at

    client.update(
        "João",
        "Silva",
        "joao@email.com"
    )

    assert client.name == "João"
    assert client.surname == "Silva"
    assert client.email == "joao@email.com"
    assert client.updated_at >= created_at


def test_should_disable_client():
    client = Client(
        "Maria",
        "Dantas",
        "maria@email.com",
        "123456",
        date(2000, 1, 1)
    )
    client.disable()

    assert client.active is False


def test_should_raise_validation_error_when_disabling_twice():
    client = Client(
        "Maria",
        "Dantas",
        "maria@email.com",
        "123456",
        date(2000, 1, 1)
    )

    client.disable()

    with pytest.raises(ValidationError):
        client.disable()


        
def test_should_convert_client_to_dict():
    client = Client(
        "Maria",
        "Dantas",
        "maria@email.com",
        "123456",
        date(2000, 1, 1)
    )

    data = client.to_dict()

    assert data["id"] == client.id
    assert data["name"] == "Maria"
    assert data["surname"] == "Dantas"
    assert data["email"] == "maria@email.com"
    assert data["birthdate"] == "2000-01-01"
    assert data["active"] is True
    assert data["created_at"] is not None
    assert data["updated_at"] is not None