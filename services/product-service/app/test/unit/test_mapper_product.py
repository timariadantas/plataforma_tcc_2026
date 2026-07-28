import pytest
from datetime import datetime, timezone
from types import SimpleNamespace

from application.mapper.product_mapper import ProductMapper
from domain.entities.product import Product


def test_should_convert_dto_to_entity():

    dto = SimpleNamespace(
        name="Notebook",
        description="Dell",
        price=5000,
        quantity=10
    )

    product = ProductMapper.to_entity(dto)

    assert isinstance(product, Product)
    assert product.name == "Notebook"
    assert product.description == "Dell"
    assert product.price == 5000
    assert product.quantity == 10
    assert product.active is True


def test_should_convert_entity_to_document():

    product = Product(
        name="Notebook",
        description="Dell",
        price=5000,
        quantity=10
    )

    document = ProductMapper.to_document(product)

    assert document["_id"] == product.id
    assert document["name"] == "Notebook"
    assert document["description"] == "Dell"
    assert document["price"] == 5000
    assert document["quantity"] == 10
    assert document["active"] is True


def test_should_convert_document_to_entity():

    now = datetime.now(timezone.utc)

    document = {
        "_id": "123",
        "name": "Notebook",
        "description": "Dell",
        "price": 5000,
        "quantity": 10,
        "created_at": now,
        "updated_at": now,
        "active": True
    }

    product = ProductMapper.from_document(document)

    assert product.id == "123"
    assert product.name == "Notebook"
    assert product.description == "Dell"
    assert product.price == 5000
    assert product.quantity == 10


def test_should_convert_entity_to_response():

    product = Product(
        name="Notebook",
        description="Dell",
        price=5000,
        quantity=10
    )

    response = ProductMapper.to_response(product)

    assert response["id"] == product.id
    assert response["name"] == "Notebook"
    assert response["description"] == "Dell"
    assert response["price"] == 5000
    assert response["quantity"] == 10