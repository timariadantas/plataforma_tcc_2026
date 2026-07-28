import pytest
from datetime import datetime , timezone

from domain.entities.product import Product

def test_create_product_successfully():
    product = Product(
        name =  "test",
        description = "test dell",
        price = 5.00,
        quantity = 10
    )
    
    assert product.name == "test"
    assert product.description == "test dell"
    assert product.price == 5.00
    assert product.quantity == 10
    assert product.active is True
    
def test_generete_id_automatically():
    product = Product(
         name =  "test",
        description = "test dell",
        price = 5.00,
        quantity = 10
    )
    assert product.id is not None
    assert isinstance(product.id, str)
    
def test_generate_created_at():
    product = Product(
         name =  "test",
        description = "test dell",
        price = 5.00,
        quantity = 10
    )  
    assert isinstance(product.created_at, datetime)
    assert product.created_at.tzinfo == timezone.utc

def test_generate_update_at():
       product = Product(
         name =  "test",
        description = "test dell",
        price = 5.00,
        quantity = 10
    ) 
       assert isinstance(product.updated_at, datetime)
       assert product.updated_at.tzinfo == timezone.utc


def test_create_inactive_product():
       product = Product(
         name =  "test",
        description = "test dell",
        price = 5.00,
        quantity = 10,
        active = False
    ) 
       assert product.active is False 
       
def test_raise_error_when_name_is_empty():
    with pytest.raises(ValueError):
        product = Product(
            name =  " ",
            description = "test dell",
            price = 5.00,
            quantity = 10
    ) 
def test_raises_error_when_name_is_blank():
    with pytest.raises(ValueError):

        Product(
            name="     ",
            description="Produto",
            price=100,
            quantity=2
        )
def test_should_raise_error_when_price_is_zero():

    with pytest.raises(ValueError):

        Product(
            name="Notebook",
            description="Produto",
            price=0,
            quantity=2
        )


def test_should_raise_error_when_price_is_negative():

    with pytest.raises(ValueError):

        Product(
            name="Notebook",
            description="Produto",
            price=-50,
            quantity=2
        )


def test_should_raise_error_when_quantity_is_negative():

    with pytest.raises(ValueError):

        Product(
            name="Notebook",
            description="Produto",
            price=100,
            quantity=-1
        )
