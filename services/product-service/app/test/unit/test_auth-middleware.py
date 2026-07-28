import pytest
from flask import Flask

from infrastructure.security.auth_middleware import token_required
from infrastructure.security.jwt_handler import JwtHandler


@pytest.fixture
def app():

    app = Flask(__name__)

    @app.route("/protected")
    @token_required
    def protected():
        return {"success": True}

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_return_401_without_token(client):

    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json["error"] == "Token missing"


def test_return_401_invalid_header(client):

    response = client.get(
        "/protected",
        headers={
            "Authorization": "Token abc"
        }
    )

    assert response.status_code == 401
    assert response.json["error"] == "Invalid authorization header"


def test_return_401_invalid_token(client):

    response = client.get(
        "/protected",
        headers={
            "Authorization": "Bearer aaa123"
        }
    )

    assert response.status_code == 401
    assert response.json["error"] == "Invalid token"


def test_return_401_expired_token(client):

    token = JwtHandler.generate_token(
        {
            "client_id": "123"
        },
        expires_minutes=-1
    )

    response = client.get(
        "/protected",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 401
    assert response.json["error"] == "Token expired"


def test_allow_valid_token(client):

    token = JwtHandler.generate_token(
        {
            "client_id": "123"
        }
    )

    response = client.get(
        "/protected",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json["success"] is True