import pytest
from datetime import datetime 
from domain.entities.client import Client

def test_create_client_sucess():
    birthdate = datetime(1990, 1, 1)
    client = Client(name="Maria", surname="Dantas", email="maria@gmail.com", birthdate=birthdate)
    
    assert client.name == "Maria"
    assert client.surname == "Dantas"
    assert client.email == "maria@gmail.com"
    assert client.active is True
    assert client.created_at is not None
    assert client.updated_at is not None
    
def test_client_update_sucess():
    birthdate = datetime(1990, 1, 1)
    client = Client(name="Leonardo", surname="Silva", email="leo@gmail.com", birthdate=birthdate)
    
    client.update("Severo", "Silva", "severo@gmail.com")
    assert client.name == "Severo"
    assert client.surname == "Silva"
    assert client.email == "severo@gmail.com"
    assert client.updated_at > client.created_at
    
def test_client_disabled():
    birthdate = datetime(1969, 7, 31)
    client = Client(name="Leonardo", surname="Silva", email="leo@gmail.com", birthdate=birthdate)
    
    client.disabled()
    assert client.active is False
    assert client.updated_at > client.created_at
    
def test_invalid_email_raises():
    birthdate = datetime(1969, 1, 2)
    with pytest.raises(Exception):
        client = Client(name="Leonardo", surname="Silva", email="leogmail.com", birthdate=birthdate)
    