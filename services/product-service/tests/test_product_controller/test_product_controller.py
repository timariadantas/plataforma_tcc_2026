import pytest
from app.api.controller.product_controller import product_blueprint

def test_create_product(client):
    client_http, mock_service = client

    mock_service.create_product.return_value = {
        "id": "123",
        "name": "Notebook",
        "description": "Dell",
        "price": 3500,
        "quantity": 5
    }

    response = client_http.post("/products", json={
        "name": "Notebook",
        "description": "Dell",
        "price": 3500,
        "quantity": 5
    })

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Notebook"
    assert data["price"] == 3500
    assert data["quantity"] == 5