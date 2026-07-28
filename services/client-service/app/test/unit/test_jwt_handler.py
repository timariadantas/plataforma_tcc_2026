import pytest
import jwt

from infrastructure.security.jwt_handler import JwtHandler

def test_generation_token():
    
    token = JwtHandler.generate_token(
        {
            "client_id": "123",
            "email": "test@email.com"
        }
    )
    
    assert token is not None
    assert isinstance(token, str)
    
def test_decode_token():
    token = JwtHandler.generate_token(
        {
            "client_id": "123",
            "email": "test@email.com"
        }
    )
    
    payload = JwtHandler.decode_token(token)
    assert payload["client_id"] == "123"
    assert payload["email"] == "test@email.com"
    
def test_raise_when_token_invalid():
    with pytest.raises(jwt.InvalidTokenError):
        JwtHandler.decode_token("aaa123")
        
def test_raise_when_token_experid():
    token = JwtHandler.generate_token(
        {
            "client_id": "123"
        }, 
        expires_minutes=-1
    )
    
    with pytest.raises(jwt.ExpiredSignatureError):
        JwtHandler.decode_token(token)