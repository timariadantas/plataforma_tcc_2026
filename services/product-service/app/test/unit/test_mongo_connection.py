import infrastructure.database.mongo_connection as mongo_connection


def test_get_database_configures_mongodb_timeout(monkeypatch):

    captured = {}

    class FakeMongoClient:

        def __init__(self, *args, **kwargs):
            captured.update(kwargs)

        def __getitem__(self, name):
            return {}

    monkeypatch.setattr(
        mongo_connection,
        "MongoClient",
        FakeMongoClient
    )

    monkeypatch.setattr(
        mongo_connection,
        "_client",
        None
    )

    monkeypatch.setenv(
        "MONGO_URI",
        "mongodb://localhost:27017"
    )

    mongo_connection.get_database()

    assert captured["serverSelectionTimeoutMS"] == 5000
    assert captured["connectTimeoutMS"] == 5000
    assert captured["socketTimeoutMS"] == 5000
    
def test_get_database_enables_mongodb_retry(monkeypatch):

    captured = {}

    class FakeMongoClient:

        def __init__(self, *args, **kwargs):
            captured.update(kwargs)

        def __getitem__(self, name):
            return {}

    monkeypatch.setattr(
        mongo_connection,
        "MongoClient",
        FakeMongoClient
    )

    monkeypatch.setattr(
        mongo_connection,
        "_client",
        None
    )

    monkeypatch.setenv(
        "MONGO_URI",
        "mongodb://localhost:27017"
    )

    mongo_connection.get_database()

    assert captured["retryWrites"] is True
    assert captured["retryReads"] is True