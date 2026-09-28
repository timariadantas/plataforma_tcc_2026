
import pytest
from unittest.mock import MagicMock

from main import app

from infrastructure.security.jwt_handler import JwtHandler

from infrastructure.errors.service_errors import (
    ProductNotFoundError,
    DatabaseUnavailableError,
    InsufficientStockError
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


def assert_success_envelope(body):

    assert "message" in body
    assert "timestamp" in body
    assert "elapsed" in body

    assert isinstance(body["message"], str)
    assert isinstance(body["timestamp"], str)
    assert isinstance(body["elapsed"], int)


def assert_error_envelope(body):

    assert "message" in body
    assert "timestamp" in body
    assert "elapsed" in body
    assert "error" in body

    assert isinstance(body["message"], str)
    assert isinstance(body["timestamp"], str)
    assert isinstance(body["elapsed"], int)
    assert isinstance(body["error"], str)


def test_create_product_success(
    client,
    token,
    monkeypatch,
    product_response
):

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
            "name": "Notebook",
            "description": "Dell",
            "price": 4500,
            "quantity": 10
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Product created successfully"

    assert body["data"]["id"] == "1"
    assert body["data"]["name"] == "Notebook"
    assert body["data"]["price"] == 4500
    assert body["data"]["quantity"] == 10

    service.create_product.assert_called_once()


def test_create_product_without_token(client):

    response = client.post(
        "/products",
        json={
            "name": "Notebook",
            "price": 1000,
            "quantity": 5
        }
    )

    assert response.status_code == 401

    body = response.get_json()

    assert_error_envelope(body)
    assert body["error"] == "Token missing"


def test_create_product_validation_error(
    client,
    token
):

    response = client.post(
        "/products",
        json={
            "name": "",
            "price": -10,
            "quantity": 5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_all_products_success(
    client,
    token,
    monkeypatch,
    product_response
):

    service = MagicMock()

    service.get_all_products.return_value = [
        product_response
    ]

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/products?page=2&limit=5",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Products retrieved successfully"

    data = body["data"]

    assert data["page"] == 2
    assert data["limit"] == 5

    assert len(data["products"]) == 1

    assert data["products"][0]["id"] == "1"
    assert data["products"][0]["name"] == "Notebook"
    assert data["products"][0]["price"] == 4500
    assert data["products"][0]["quantity"] == 10

    service.get_all_products.assert_called_once_with(2, 5)


def test_get_all_products_database_error(
    client,
    token,
    monkeypatch
):

    service = MagicMock()

    service.get_all_products.side_effect = (
        DatabaseUnavailableError(
            "Database unavailable"
        )
    )

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/products",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 503

    body = response.get_json()

    assert_error_envelope(body)

    assert body["error"] == "Database unavailable"


def test_get_all_products_invalid_page(
    client,
    token
):

    response = client.get(
        "/products?page=abc&limit=10",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_all_products_invalid_limit(
    client,
    token
):

    response = client.get(
        "/products?page=1&limit=abc",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_all_products_invalid_page_zero(
    client,
    token
):

    response = client.get(
        "/products?page=0&limit=10",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_all_products_invalid_limit_zero(
    client,
    token
):

    response = client.get(
        "/products?page=1&limit=0",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_inactive_products_success(
    client,
    token,
    monkeypatch,
    product_response
):

    service = MagicMock()

    service.get_inactive_products.return_value = [
        product_response
    ]

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/products/inactive",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Inactive products retrieved successfully"

    data = body["data"]

    assert data["page"] == 1
    assert data["limit"] == 10

    assert len(data["products"]) == 1

    assert data["products"][0]["id"] == "1"
    assert data["products"][0]["name"] == "Notebook"

    service.get_inactive_products.assert_called_once_with(
        1,
        10
    )


def test_get_inactive_products_invalid_page(
    client,
    token
):

    response = client.get(
        "/products/inactive?page=abc&limit=10",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_inactive_products_invalid_limit(
    client,
    token
):

    response = client.get(
        "/products/inactive?page=1&limit=abc",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_inactive_products_invalid_page_zero(
    client,
    token
):

    response = client.get(
        "/products/inactive?page=0&limit=10",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_inactive_products_invalid_limit_zero(
    client,
    token
):

    response = client.get(
        "/products/inactive?page=1&limit=0",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_get_inactive_products_without_token(client):

    response = client.get(
        "/products/inactive"
    )

    assert response.status_code == 401

    body = response.get_json()

    assert_error_envelope(body)


def test_get_product_success(
    client,
    token,
    monkeypatch,
    product_response
):

    service = MagicMock()

    service.get_product_by_id.return_value = product_response

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/products/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Product found"

    assert body["data"]["id"] == "1"
    assert body["data"]["name"] == "Notebook"
    assert body["data"]["price"] == 4500

    service.get_product_by_id.assert_called_once_with("1")


def test_get_product_not_found(
    client,
    token,
    monkeypatch
):

    service = MagicMock()

    service.get_product_by_id.side_effect = (
        ProductNotFoundError(
            "Product not found"
        )
    )

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/products/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    body = response.get_json()

    assert_error_envelope(body)

    assert body["message"] == "Product not found"
    assert body["error"] == "Product not found"


def test_update_product_success(
    client,
    token,
    monkeypatch,
    product_response
):

    service = MagicMock()

    service.update_product.return_value = product_response

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.put(
        "/products/1",
        json={
            "name": "Notebook",
            "description": "Dell",
            "price": 4500,
            "quantity": 20
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Product updated successfully"

    assert body["data"]["id"] == "1"
    assert body["data"]["name"] == "Notebook"
    assert body["data"]["price"] == 4500
    assert body["data"]["quantity"] == 10

    service.update_product.assert_called_once()


def test_update_product_validation_error(
    client,
    token
):

    response = client.put(
        "/products/1",
        json={
            "name": "",
            "price": -1,
            "quantity": 5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_delete_product_success(
    client,
    token,
    monkeypatch
):

    service = MagicMock()

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.delete(
        "/products/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Product deleted successfully"

    assert "data" not in body

    service.delete_product.assert_called_once_with("1")


def test_delete_product_not_found(
    client,
    token,
    monkeypatch
):

    service = MagicMock()

    service.delete_product.side_effect = (
        ProductNotFoundError(
            "Product not found"
        )
    )

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.delete(
        "/products/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    body = response.get_json()

    assert_error_envelope(body)


def test_decrease_stock_success(
    client,
    token,
    monkeypatch
):

    service = MagicMock()

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.patch(
        "/products/1/decrease-stock",
        json={
            "quantity": 2
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Stock updated successfully"
    assert "data" not in body

    service.decrease_stock.assert_called_once_with(
        "1",
        2
    )


def test_decrease_stock_insufficient(
    client,
    token,
    monkeypatch
):

    service = MagicMock()

    service.decrease_stock.side_effect = (
        InsufficientStockError(
            "Insufficient stock"
        )
    )

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.patch(
        "/products/1/decrease-stock",
        json={
            "quantity": 100
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 409

    body = response.get_json()

    assert_error_envelope(body)

    assert body["error"] == "Insufficient stock"


def test_decrease_stock_invalid_quantity(
    client,
    token
):

    response = client.patch(
        "/products/1/decrease-stock",
        json={
            "quantity": 0
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_internal_get_product_success(
    client,
    monkeypatch,
    product_response
):

    service = MagicMock()

    service.get_product_by_id.return_value = product_response

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/internal/products/1"
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Product found"

    assert body["data"]["id"] == "1"
    assert body["data"]["name"] == "Notebook"
    assert body["data"]["price"] == 4500
    assert body["data"]["quantity"] == 10

    service.get_product_by_id.assert_called_once_with("1")


def test_internal_get_product_not_found(
    client,
    monkeypatch
):

    service = MagicMock()

    service.get_product_by_id.side_effect = (
        ProductNotFoundError(
            "Product not found"
        )
    )

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/internal/products/1"
    )

    assert response.status_code == 404

    body = response.get_json()

    assert_error_envelope(body)

    assert body["message"] == "Product not found"
    assert body["error"] == "Product not found"


def test_internal_decrease_stock_success(
    client,
    monkeypatch
):

    service = MagicMock()

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.patch(
        "/internal/products/1/decrease-stock",
        json={
            "quantity": 2
        }
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Stock updated successfully"

    assert "data" not in body

    service.decrease_stock.assert_called_once_with(
        "1",
        2
    )


def test_internal_decrease_stock_insufficient(
    client,
    monkeypatch
):

    service = MagicMock()

    service.decrease_stock.side_effect = (
        InsufficientStockError(
            "Insufficient stock"
        )
    )

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.patch(
        "/internal/products/1/decrease-stock",
        json={
            "quantity": 100
        }
    )

    assert response.status_code == 409

    body = response.get_json()

    assert_error_envelope(body)

    assert body["error"] == "Insufficient stock"


def test_internal_decrease_stock_invalid_quantity(
    client
):

    response = client.patch(
        "/internal/products/1/decrease-stock",
        json={
            "quantity": 0
        }
    )

    assert response.status_code == 400

    body = response.get_json()

    assert_error_envelope(body)


def test_internal_get_stock_success(
    client,
    monkeypatch,
    product_response
):

    service = MagicMock()

    service.get_product_by_id.return_value = product_response

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/internal/products/1/stock"
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Stock found"

    assert body["data"]["quantity"] == 10

    service.get_product_by_id.assert_called_once_with("1")


def test_internal_get_stock_not_found(
    client,
    monkeypatch
):

    service = MagicMock()

    service.get_product_by_id.side_effect = (
        ProductNotFoundError(
            "Product not found"
        )
    )

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/internal/products/1/stock"
    )

    assert response.status_code == 404

    body = response.get_json()

    assert_error_envelope(body)

    assert body["message"] == "Product not found"
    assert body["error"] == "Product not found"


def test_internal_get_price_success(
    client,
    monkeypatch,
    product_response
):

    service = MagicMock()

    service.get_product_by_id.return_value = product_response

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/internal/products/1/price"
    )

    assert response.status_code == 200

    body = response.get_json()

    assert_success_envelope(body)

    assert body["message"] == "Price found"

    assert body["data"]["price"] == 4500

    service.get_product_by_id.assert_called_once_with("1")


def test_internal_get_price_not_found(
    client,
    monkeypatch
):

    service = MagicMock()

    service.get_product_by_id.side_effect = (
        ProductNotFoundError(
            "Product not found"
        )
    )

    monkeypatch.setattr(
        controller,
        "get_service",
        lambda: service
    )

    response = client.get(
        "/internal/products/1/price"
    )

    assert response.status_code == 404

    body = response.get_json()

    assert_error_envelope(body)

    assert body["message"] == "Product not found"
    assert body["error"] == "Product not found"
