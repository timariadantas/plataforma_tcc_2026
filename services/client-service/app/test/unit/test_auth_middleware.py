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
        return {"success" : True}
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_return_401_without_token(client):
    response = client.get("/protected")
    
    assert response.status_code == 401
    
def test_return_401_invalid_token(client):
    response = client.get(
        "/protected",
        headers={
            "Authorization": "Bearer aa123"
        }
    )
    assert response.status_code == 401
    
def test_allow_valid_token(client):
    token = JwtHandler.generate_token({
        "client_id": "123"
    })
    
    response = client.get(
        "/protected",
        headers={
        "Authorization":f"Bearer {token}"
        }
    )
    assert response.status_code == 200