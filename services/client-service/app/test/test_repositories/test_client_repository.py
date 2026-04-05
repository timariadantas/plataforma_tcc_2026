import uuid
from datetime import datetime

from domain.entities.client import Client
from infrastructure.repositories.client_repository import ClientRepository
from infrastructure.database.connection import DatabaseConnection

def create_test_client():
    return Client(
        name = "Teste",
        surname= "Testee",
        email=f"test{uuid.uuid4()}@email.com", 
        birthdate = datetime(1993, 1, 1)
        
    )
    
def test_save_and_get_by_id():
    db = DatabaseConnection()
    repo = ClientRepository()
    client = create_test_client()
    
    with db.get_connection() as conn:
        repo.save(client, conn)
        conn.commit()
        
        result = repo.get_by_id(client.id, conn)
        
        assert result is not None
        assert result.id == client.id
        assert result.email == client.email
    

def test_get_all_clients():
    db = DatabaseConnection()
    repo = ClientRepository ()
    
    client = create_test_client()
    
    with db.get_connection() as conn:
        repo.save(client, conn)
        conn.commit()
        
        results = repo.get_all(conn)
        assert len(results) > 0

def test_update_client():
    db = DatabaseConnection()
    repo = ClientRepository()

    client = create_test_client()

    with db.get_connection() as conn:
        repo.save(client, conn)
        conn.commit()

        # atualiza dados
        client.update("NovoNome", "NovoSobrenome", "novo@email.com")
        repo.update(client, conn)
        conn.commit()

        updated = repo.get_by_id(client.id, conn)

        assert updated.name == "NovoNome"
        assert updated.email == "novo@email.com"

def test_delete_client():
    db = DatabaseConnection()
    repo = ClientRepository()

    client = create_test_client()

    with db.get_connection() as conn:
        repo.save(client, conn)
        conn.commit()

        repo.delete(client.id, conn)
        conn.commit()

        deleted = repo.get_by_id(client.id, conn)

        assert deleted.active is False
def test_get_active_clients():
    db = DatabaseConnection()
    repo = ClientRepository()

    client = create_test_client()

    with db.get_connection() as conn:
        repo.save(client, conn)
        conn.commit()

        results = repo.get_all_active(conn)

        assert any(c.id == client.id for c in results)


def test_get_inactive_clients():
    db = DatabaseConnection()
    repo = ClientRepository()

    client = create_test_client()

    with db.get_connection() as conn:
        repo.save(client, conn)
        conn.commit()

        repo.delete(client.id, conn)
        conn.commit()

        results = repo.get_all_inactive(conn)

        assert any(c.id == client.id for c in results)       