import pytest
from unittest.mock import MagicMock
from datetime import date, datetime, timezone

from infrastructure.repositories.client_repository import ClientRepository
from domain.entities.client import Client
import ulid 

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
    sql, params = cursor.execute.call_args.args

    assert params["id"] == client.id
    assert len(params["id"]) == 26
    
def test_save_client_should_persist_ulid(repository):
    repo, db, conn, cursor = repository

    client = Client(
        "Maria",
        "Dantas",
        "maria@email.com",
        "112233",
        date(1993, 1, 5)
    )

    repo.save(client)

    cursor.execute.assert_called_once()

    sql, params = cursor.execute.call_args.args

    assert params["id"] == client.id
    assert len(params["id"]) == 26

    conn.commit.assert_called_once()
    
def test_save_client_should_preserve_existing_ulid(repository):
    repo, db, conn, cursor = repository

    client_id = "01KZSSCHCT24Q1YZ7P9PDTRCZW"

    client = Client(
        "Maria",
        "Dantas",
        "maria@email.com",
        "112233",
        date(1993, 1, 5),
        id=client_id
    )

    repo.save(client)

    _, params = cursor.execute.call_args.args

    assert params["id"] == client_id
    
def test_get_client_by_id(repository):
    repo, db, conn, cursor = repository 
    client_id = "01KZSSCHCT24Q1YZ7P9PDTRCZW"
    
    cursor.fetchone.return_value = (
        client_id,
        "test",
        "tests",
        "email@email.com",
        "112233", 
        date(1993,1,5),
        
        1,
        datetime.now(timezone.utc),
        datetime.now(timezone.utc)
        
    )
    client = repo.get_by_id(client_id)
    
    assert client is not None
    assert client.id == client_id
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

    client_id = "01KZSSCHCT24Q1YZ7P9PDTRCZW"

    created_at = datetime(
        2025,
        1,
        10,
        tzinfo=timezone.utc
    )

    updated_at = datetime(
        2025,
        1,
        15,
        tzinfo=timezone.utc
    )

    row = (
        client_id,
        "Maria",
        "Dantas",
        "maria@email.com",
        "112233",
        date(1993, 1, 5),
        1,
        created_at,
        updated_at
    )

    client = repo._map_to_entity(row)

    assert client.id == client_id
    assert client.name == "Maria"
    assert client.surname == "Dantas"
    assert client.email == "maria@email.com"
    assert client.password_hash == "112233"
    assert client.birthdate == date(1993, 1, 5)
    assert client.active is True
    assert client.created_at == created_at
    assert client.updated_at == updated_at
    
def test_mapper_should_preserve_existing_ulid(repository):

    repo, _, _, _ = repository

    client_id = "01KZSSCHCT24Q1YZ7P9PDTRCZW"

    row = (
        client_id,
        "Maria",
        "Dantas",
        "maria@email.com",
        "112233",
        date(1993, 1, 5),
        1,
        datetime.now(timezone.utc),
        datetime.now(timezone.utc)
    )

    client = repo._map_to_entity(row)

    assert client.id == client_id
    assert len(client.id) == 26