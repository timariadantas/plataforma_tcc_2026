import pytest
from unittest.mock import MagicMock
from datetime import date, datetime, timezone

from infrastructure.repositories.client_repository import ClientRepository
from domain.entities.client import Client

@pytest.fixture
def repository():
    db = MagicMock()
    
    conn = MagicMock()
    cursor = MagicMock()
    
    db.get_connection.return_value.__enter__.return_value = conn
    
    conn.cursor.return_value = cursor
    
    repo = ClientRepository(db)
    
    return repo, db, conn , cursor

def test_save_client(repository):
    repo, db, conn, cursor = repository 
    client = Client (
        "test", 
        "tests",
        "email@email.com",
        "112233",
        date(1993,1,5)
        
    )
    repo.save(client)
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()
    
def test_get_client_by_id(repository):
    repo, db, conn, cursor = repository 
    cursor.fetchone.return_value = (
        "1",
        "test",
        "tests",
        "email@email.com",
        "112233", 
        date(1993,1,5),
        
        1,
        datetime.now(timezone.utc),
        datetime.now(timezone.utc)
        
    )
    client = repo.get_by_id("1")
    assert client.id == "1"
    assert client.email == "email@email.com"
    
    
def test_return_none_when_client_not_found(repository):
    repo, db, conn, cursor = repository
    
    cursor.fetchone.return_value = None
    result = repo.get_by_id("10")
    
    assert result is None
    

def test_get_all_client(repository):
    repo, db, conn, cursor = repository 
    
    row = (
        "1",
        "test",
        "tests",
        "email@email.com",
        "112233", 
        date(1993,1,5),
        
        1,
        datetime.now(timezone.utc),
        datetime.now(timezone.utc)
    )
    
    cursor.fetchall.return_value = [row]
    result = repo.get_all()
    
    assert len(result) == 1
    
def test_update_client(repository):
    repo, db, conn, cursor = repository 
    client = Client(
        "test",
        "tests",
        "email@email.com",
        "112233", 
        date(1993,1,5)
    )
    client.id = "1"
    repo.update(client)
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()
    
def test_delete_client(repository):
    repo, db, conn, cursor = repository 
    
    repo.delete("1")
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()
    
def test_update_password(repository):
    repo, db, conn, cursor = repository 
    
    repo.update_password("1", "nova_senha")
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()
    
def test_get_client_by_email(repository):

    repo, db, conn, cursor = repository
    cursor.fetchone.return_value = (

        "1",

        "test",

        "tests",

        "email@email.com",

        "112233",

        date(1993,1,5),

        1,

        datetime.now(timezone.utc),
        datetime.now(timezone.utc)

    )

    client = repo.get_by_email("email@email.com")

    assert client.email == "email@email.com"
    
def test_get_all_active_clients(repository):
    repo, db, conn, cursor = repository

    row = (
        "1",
        "test",
        "tests",
        "email@email.com",
        "112233",
        date(1993,1,5),
        1,
        datetime.now(timezone.utc),
        datetime.now(timezone.utc)
    )

    cursor.fetchall.return_value = [row]

    clients = repo.get_all_active()

    assert len(clients) == 1
    assert clients[0].active is True
    cursor.execute.assert_called_once()
    
def test_map_database_row_to_entity(repository):

    repo, _, _, _ = repository

    row = (
         "1",
        "test",
        "tests",
        "email@email.com",
        "112233",
        date(1993,1,5),
        1,
        datetime.now(timezone.utc),
        datetime.now(timezone.utc)

    )

    client = repo._map_to_entity(row)

    assert client.id == "1"

    assert client.birthdate == date(1993,1,5)