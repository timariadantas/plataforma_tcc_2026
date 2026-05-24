import pytest
from app.domain.entities.product import Product


def test_product_entity_valid():
    product = Product(
        name="Notebook",
        description="Dell",
        price=3500,
        quantity=10
    )

    assert product.name == "Notebook"
    assert product.price == 3500
    assert product.quantity == 10
    assert product.active is True


def test_product_entity_invalid_price():
    with pytest.raises(ValueError):
        Product(
            name="Notebook",
            description="Dell",
            price=0,
            quantity=10
        )


def test_product_entity_invalid_quantity():
    with pytest.raises(ValueError):
        Product(
            name="Notebook",
            description="Dell",
            price=100,
            quantity=-1
        )


def test_product_entity_empty_name():
    with pytest.raises(ValueError):
        Product(
            name="",
            description="Dell",
            price=100,
            quantity=1
        )