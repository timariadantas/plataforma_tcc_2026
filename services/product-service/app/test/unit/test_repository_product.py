import mongomock
import pytest

from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.errors.service_errors import (
    InsufficientStockError,
    ProductNotFoundError,
)
from domain.entities.product import Product


@pytest.fixture
def repository():
    db = mongomock.MongoClient(tz_aware=True).db
    return ProductRepository(db)


def test_save_product(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    saved = repository.collection.find_one({
        "_id": product.id
    })

    assert saved is not None
    assert saved["name"] == "Notebook"
    assert saved["active"] is True


def test_find_product_by_id(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    result = repository.find_by_id(product.id)

    assert result.id == product.id
    assert result.name == "Notebook"


def test_raise_when_product_not_found(repository):

    with pytest.raises(ProductNotFoundError):
        repository.find_by_id("123")


def test_find_all_products_returns_only_active_products(repository):

    active_product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10,
        active=True
    )

    inactive_product = Product(
        name="Mouse antigo",
        description="Logitech",
        price=100,
        quantity=30,
        active=False
    )

    repository.save(active_product)
    repository.save(inactive_product)

    products = repository.find_all()

    assert len(products) == 1
    assert products[0].id == active_product.id
    assert products[0].active is True


def test_find_inactive_products(repository):

    active_product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10,
        active=True
    )

    inactive_product = Product(
        name="Mouse antigo",
        description="Logitech",
        price=100,
        quantity=30,
        active=False
    )

    repository.save(active_product)
    repository.save(inactive_product)

    products = repository.find_inactive()

    assert len(products) == 1
    assert products[0].id == inactive_product.id
    assert products[0].active is False


def test_find_all_products_pagination(repository):

    for i in range(5):
        repository.save(
            Product(
                name=f"Product {i}",
                description="Test",
                price=100,
                quantity=10
            )
        )

    products = repository.find_all(
        page=2,
        limit=2
    )

    assert len(products) == 2


def test_find_inactive_products_pagination(repository):

    for i in range(5):
        repository.save(
            Product(
                name=f"Product {i}",
                description="Test",
                price=100,
                quantity=10,
                active=False
            )
        )

    products = repository.find_inactive(
        page=2,
        limit=2
    )

    assert len(products) == 2


def test_update_product(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    original_updated_at = product.updated_at.replace(
    microsecond=(product.updated_at.microsecond // 1000) * 1000
)

    repository.update(
        product.id,
        {
            "price": 5000
        }
    )

    updated = repository.find_by_id(product.id)

    assert updated.price == 5000
    assert updated.updated_at >= original_updated_at


def test_delete_product(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    repository.delete(product.id)

    doc = repository.collection.find_one({
        "_id": product.id
    })

    assert doc["active"] is False


def test_deleted_product_does_not_appear_in_find_all(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    repository.delete(product.id)

    products = repository.find_all()

    assert len(products) == 0


def test_deleted_product_appears_in_find_inactive(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    repository.delete(product.id)

    products = repository.find_inactive()

    assert len(products) == 1
    assert products[0].id == product.id
    assert products[0].active is False


def test_decrease_stock(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    repository.decrease_stock(product.id, 3)

    updated = repository.find_by_id(product.id)

    assert updated.quantity == 7


def test_raise_when_stock_is_insufficient(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=2
    )

    repository.save(product)

    with pytest.raises(InsufficientStockError):

        repository.decrease_stock(
            product.id,
            5
        )

    updated = repository.find_by_id(product.id)

    assert updated.quantity == 2


def test_delete_product_not_found(repository):

    with pytest.raises(ProductNotFoundError):

        repository.delete("abc")


def test_update_product_not_found(repository):

    with pytest.raises(ProductNotFoundError):

        repository.update(
            "abc",
            {
                "price": 100
            }
        )