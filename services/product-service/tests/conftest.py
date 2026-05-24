import pytest
import mongomock
from unittest.mock import Mock

from app.infrastructure.repositories.product_repository import ProductRepository
from app.application.service.product_service import ProductService
from app.main import app


# =========================
# REPOSITORY TEST (MONGOMOCK)
# =========================
@pytest.fixture
def repo():
    client = mongomock.MongoClient()
    db = client["test_db"]

    repository = ProductRepository(db)

    repository.collection.delete_many({})

    return repository


# =========================
# SERVICE TEST
# =========================
@pytest.fixture
def repository_mock():
    return Mock()


@pytest.fixture
def service(repository_mock):
    return ProductService(repository_mock)


# =========================
# CONTROLLER TEST
# =========================
@pytest.fixture
def client(monkeypatch):

    mock_service = Mock()

    def fake_get_service():
        return mock_service

    monkeypatch.setattr(
        "app.api.controller.product_controller.get_service",
        fake_get_service
    )

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client, mock_service