import pytest
from unittest.mock import Mock


def test_create_product_success(service, repository_mock):
    dto = Mock()
    dto.price = 100
    dto.quantity = 5

    service.create_product(dto)

    repository_mock.save.assert_called_once()