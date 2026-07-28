import mongomock
import pytest

from infrastructure.repositories.product_repository import ProductRepository
from domain.entities.product import Product


@pytest.fixture
def repository():
    db = mongomock.MongoClient().db
    return ProductRepository(db)

def test_save_product(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    saved = repository.collection.find_one({"_id": product.id})

    assert saved is not None
    assert saved["name"] == "Notebook"
    
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
    
import pytest

from infrastructure.errors.service_errors import ProductNotFoundError


def test_raise_when_product_not_found(repository):

    with pytest.raises(ProductNotFoundError):
        repository.find_by_id("123")

def test_find_all_products(repository):

    repository.save(Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    ))

    repository.save(Product(
        name="Mouse",
        description="Logitech",
        price=100,
        quantity=30
    ))

    products = repository.find_all()

    assert len(products) == 2
    
def test_update_product(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    repository.update(product.id, {
        "price":5000
    })

    updated = repository.find_by_id(product.id)

    assert updated.price == 5000
    
def test_delete_product(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=10
    )

    repository.save(product)

    repository.delete(product.id)

    doc = repository.collection.find_one({"_id":product.id})

    assert doc["active"] is False
    
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
    
from infrastructure.errors.service_errors import InsufficientStockError


def test_raise_when_stock_is_insufficient(repository):

    product = Product(
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=2
    )

    repository.save(product)

    with pytest.raises(InsufficientStockError):
        repository.decrease_stock(product.id, 5)
        
def test_delete_product_not_found(repository):

    with pytest.raises(ProductNotFoundError):
        repository.delete("abc")

def test_update_product_not_found(repository):

    with pytest.raises(ProductNotFoundError):
        repository.update("abc", {"price":100})