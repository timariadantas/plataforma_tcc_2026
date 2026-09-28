import time

import pytest

from flask import Flask, g

from infrastructure.security.auth_middleware import token_required
from infrastructure.security.jwt_handler import JwtHandler

from api.middleware.exception_middleware import register_exception_handlers


@pytest.fixture
def app():

    app = Flask(__name__)

    @app.before_request
    def start_request_timer():
        g.start_time = time.perf_counter()

    register_exception_handlers(app)

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

    data = response.get_json()

    assert data["message"] == "Request failed"
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["elapsed"], int)

    assert data["error"] == "Authentication required"

    assert "data" not in data


def test_return_401_invalid_token(client):

    response = client.get(
        "/protected",
        headers={
            "Authorization": "Bearer aa123"
        }
    )

    assert response.status_code == 401

    data = response.get_json()

    assert data["message"] == "Request failed"
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["elapsed"], int)

    assert data["error"] == "Invalid token"

    assert "data" not in data


def test_allow_valid_token(client):

    token = JwtHandler.generate_token({
        "client_id": "123"
    })

    response = client.get(
        "/protected",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

