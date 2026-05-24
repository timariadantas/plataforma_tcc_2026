from app.domain.entities.product import Product


def test_save_product(repo):
    product = Product("Notebook", "Dell", 3500, 5)

    repo.save(product)

    saved = repo.collection.find_one({"_id": product.id})

    assert saved is not None
    assert saved["name"] == "Notebook"
    assert saved["price"] == 3500


def test_find_by_id(repo):
    product = Product("Mouse", "Logitech", 100, 10)

    repo.save(product)

    found = repo.find_by_id(product.id)

    assert found.name == "Mouse"
    assert found.price == 100


def test_find_all(repo):
    repo.save(Product("A", "desc", 10, 1))
    repo.save(Product("B", "desc", 20, 2))

    result = repo.find_all()

    assert len(result) == 2


def test_update_product(repo):
    product = Product("A", "desc", 10, 1)

    repo.save(product)

    repo.update(product.id, {"name": "Updated"})

    updated = repo.collection.find_one({"_id": product.id})

    assert updated["name"] == "Updated"


def test_delete_product(repo):
    product = Product("A", "desc", 10, 1)

    repo.save(product)
    repo.delete(product.id)

    updated = repo.collection.find_one({"_id": product.id})

    assert updated["active"] is False


def test_decrease_stock(repo):
    product = Product("A", "desc", 10, 10)

    repo.save(product)
    repo.decrease_stock(product.id, 3)

    updated = repo.collection.find_one({"_id": product.id})

    assert updated["quantity"] == 7