import time

import pytest
from flask import Flask

from infrastructure.security.auth_middleware import token_required
from infrastructure.security.jwt_handler import JwtHandler


@pytest.fixture
def app():

    app = Flask(__name__)

    @app.before_request
    def start_request_timer():
        from flask import g
        g.start_time = time.perf_counter()

    @app.route("/protected")
    @token_required
    def protected():
        return {
            "success": True
        }

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_return_401_without_token(client):

    response = client.get("/protected")

    assert response.status_code == 401

    body = response.get_json()

    assert body["message"] == "Request failed"
    assert body["error"] == "Token missing"
    assert "timestamp" in body
    assert isinstance(body["elapsed"], int)


def test_return_401_invalid_header(client):

    response = client.get(
        "/protected",
        headers={
            "Authorization": "Token abc"
        }
    )

    assert response.status_code == 401

    body = response.get_json()

    assert body["message"] == "Request failed"
    assert body["error"] == "Invalid authorization header"
    assert "timestamp" in body
    assert isinstance(body["elapsed"], int)


def test_return_401_invalid_token(client):

    response = client.get(
        "/protected",
        headers={
            "Authorization": "Bearer aaa123"
        }
    )

    assert response.status_code == 401

    body = response.get_json()

    assert body["message"] == "Request failed"
    assert body["error"] == "Invalid token"
    assert "timestamp" in body
    assert isinstance(body["elapsed"], int)


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

    body = response.get_json()

    assert body["message"] == "Request failed"
    assert body["error"] == "Token expired"
    assert "timestamp" in body
    assert isinstance(body["elapsed"], int)


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

    body = response.get_json()

    assert body["success"] is True