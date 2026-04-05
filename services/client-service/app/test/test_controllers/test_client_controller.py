import pytest
from main import app  

@pytest.fixture
def client():
    return app.test_client()
def test_create_client(client):
    response = client.post("/clients", json={
        "name": "Carlos",
        "surname": "Dantas",
        "email": "teste_controller@email.com",
        "birthdate": "1990-01-01"
    })

    assert response.status_code == 201
    assert "id" in response.json



def test_get_client(client):
    create = client.post("/clients", json={
        "name": "Carlos",
        "surname": "Dantas",
        "email": "teste_get@email.com",
        "birthdate": "1990-01-01"
    })

    client_id = create.json["id"]

    response = client.get(f"/clients/{client_id}")

    assert response.status_code == 200
    assert response.json["id"] == client_id



def test_get_all_clients(client):
    response = client.get("/clients")

    assert response.status_code == 200
    assert isinstance(response.json, list)



def test_update_client(client):
    create = client.post("/clients", json={
        "name": "Carlos",
        "surname": "Dantas",
        "email": "teste_update@email.com",
        "birthdate": "1990-01-01"
    })

    client_id = create.json["id"]

    response = client.put(f"/clients/{client_id}", json={
        "name": "Novo",
        "surname": "Nome",
        "email": "novo@email.com",
        "birthdate": "1990-01-01"
    })

    assert response.status_code == 200



def test_delete_client(client):
    create = client.post("/clients", json={
        "name": "Carlos",
        "surname": "Dantas",
        "email": "teste_delete@email.com",
        "birthdate": "1990-01-01"
    })

    client_id = create.json["id"]

    response = client.delete(f"/clients/{client_id}")

    assert response.status_code == 200