import pytest
from unittest.mock import MagicMock
from types import SimpleNamespace


from application.service.product_service import ProductService
from infrastructure.errors.service_errors import InvalidProductDataError


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def service(repository):
    return ProductService(repository)


@pytest.fixture
def dto():
    return SimpleNamespace(
        name="Notebook",
        description="Notebook Dell",
        price=4500,
        quantity=10
    )


def test_create_product_successfully(service, repository, dto):

    response = service.create_product(dto, "user-123")

    repository.save.assert_called_once()

    assert response["name"] == "Notebook"
    assert response["price"] == 4500


def test_raise_error_when_price_is_zero(service, dto):

    dto.price = 0

    with pytest.raises(InvalidProductDataError):
        service.create_product(dto, "user-123")


def test_raise_error_when_price_is_negative(service, dto):

    dto.price = -10

    with pytest.raises(InvalidProductDataError):
        service.create_product(dto, "user-123")


def test_raise_error_when_quantity_is_negative(service, dto):

    dto.quantity = -1

    with pytest.raises(InvalidProductDataError):
        service.create_product(dto, "user-123")


def test_get_all_products(service, repository):

    repository.find_all.return_value = [
        SimpleNamespace(
            id="1",
            name="Notebook",
            description="Dell",
            price=4500,
            quantity=5
        )
    ]

    products = service.get_all_products(1, 10)

    repository.find_all.assert_called_once_with(1, 10)

    assert len(products) == 1
    assert products[0]["name"] == "Notebook"


def test_get_product_by_id(service, repository):

    repository.find_by_id.return_value = SimpleNamespace(
        id="1",
        name="Notebook",
        description="Dell",
        price=4500,
        quantity=5
    )

    product = service.get_product_by_id("1")

    repository.find_by_id.assert_called_once_with("1")

    assert product["id"] == "1"


def test_update_product(service, repository):

    dto = MagicMock()

    dto.model_dump.return_value = {
        "name": "Notebook",
        "description": "Notebook Dell",
        "price": 4500,
        "quantity": 10
    }

    service.update_product("1", dto)

    repository.update.assert_called_once()

    args = repository.update.call_args[0]

    assert args[0] == "1"
    assert args[1]["name"] == "Notebook"
    assert "updated_at" in args[1]

def test_delete_product(service, repository):

    service.delete_product("1")

    repository.delete.assert_called_once_with("1")


def test_decrease_stock(service, repository):

    service.decrease_stock("1", 2)

    repository.decrease_stock.assert_called_once_with("1", 2)


def test_raise_error_when_decrease_stock_quantity_is_zero(service):

    with pytest.raises(InvalidProductDataError):

        service.decrease_stock("1", 0)


def test_raise_error_when_decrease_stock_quantity_is_negative(service):

    with pytest.raises(InvalidProductDataError):

        service.decrease_stock("1", -5)