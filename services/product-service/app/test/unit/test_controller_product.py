import pytest
from unittest.mock import MagicMock

from main import app

from infrastructure.security.jwt_handler import JwtHandler
from infrastructure.errors.service_errors import (
    ProductNotFoundError,
    DatabaseUnavailableError,
    InsufficientStockError,
    InvalidProductDataError
)

import api.controller.product_controller as controller


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def token():
    return JwtHandler.generate_token({
        "client_id": "123"
    })


@pytest.fixture
def product_response():

    return {
        "id": "1",
        "name": "Notebook",
        "description": "Dell",
        "price": 4500,
        "quantity": 10
    }


# =========================
# POST /products
# =========================


def test_create_product_success(
        client,
        token,
        monkeypatch,
        product_response):

    service = MagicMock()

    service.create_product.return_value = product_response


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )


    response = client.post(
        "/products",
        json={
            "name":"Notebook",
            "description":"Dell",
            "price":4500,
            "quantity":10
        },
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 201



def test_create_product_without_token(client):

    response = client.post(
        "/products",
        json={
            "name":"Notebook",
            "price":1000,
            "quantity":5
        }
    )


    assert response.status_code == 401



def test_create_product_validation_error(
        client,
        token):


    response = client.post(
        "/products",
        json={
            "name":"",
            "price":-10,
            "quantity":5
        },
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 400



# =========================
# GET ALL
# =========================


def test_get_all_products_success(
        client,
        token,
        monkeypatch,
        product_response):


    service = MagicMock()

    service.get_all_products.return_value=[
        product_response
    ]


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.get(
        "/products",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 200



def test_get_all_products_database_error(
        client,
        token,
        monkeypatch):


    service = MagicMock()

    service.get_all_products.side_effect = (
        DatabaseUnavailableError(
            "Database unavailable"
        )
    )


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.get(
        "/products",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 500



# =========================
# GET ID
# =========================


def test_get_product_success(
        client,
        token,
        monkeypatch,
        product_response):


    service = MagicMock()

    service.get_product_by_id.return_value = product_response


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.get(
        "/products/1",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 200



def test_get_product_not_found(
        client,
        token,
        monkeypatch):


    service = MagicMock()

    service.get_product_by_id.side_effect = (
        ProductNotFoundError(
            "Product not found"
        )
    )


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.get(
        "/products/1",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 404



# =========================
# PUT
# =========================


def test_update_product_success(
        client,
        token,
        monkeypatch):


    service = MagicMock()


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.put(
        "/products/1",
        json={
            "name":"Notebook",
            "description":"Dell",
            "price":4500,
            "quantity":20
        },
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 200



def test_update_product_validation_error(
        client,
        token):


    response = client.put(
        "/products/1",
        json={
            "name":"",
            "price":-1,
            "quantity":5
        },
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 400



# =========================
# DELETE
# =========================


def test_delete_product_success(
        client,
        token,
        monkeypatch):


    service = MagicMock()


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.delete(
        "/products/1",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 200



def test_delete_product_not_found(
        client,
        token,
        monkeypatch):


    service = MagicMock()

    service.delete_product.side_effect = (
        ProductNotFoundError(
            "Product not found"
        )
    )


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.delete(
        "/products/1",
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 404



# =========================
# PATCH decrease stock
# =========================


def test_decrease_stock_success(
        client,
        token,
        monkeypatch):


    service = MagicMock()


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.patch(
        "/products/1/decrease-stock",
        json={
            "quantity":2
        },
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 200



def test_decrease_stock_insufficient(
        client,
        token,
        monkeypatch):


    service = MagicMock()

    service.decrease_stock.side_effect = (
        InsufficientStockError(
            "Insufficient stock"
        )
    )


    monkeypatch.setattr(
        controller,
        "get_service",
        lambda:service
    )


    response = client.patch(
        "/products/1/decrease-stock",
        json={
            "quantity":100
        },
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 400



def test_decrease_stock_invalid_quantity(
        client,
        token):


    response = client.patch(
        "/products/1/decrease-stock",
        json={
            "quantity":0
        },
        headers={
            "Authorization":f"Bearer {token}"
        }
    )


    assert response.status_code == 400