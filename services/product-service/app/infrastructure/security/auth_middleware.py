from flask import request, jsonify
from functools import wraps
from infrastructure.security.jwt_handler import JwtHandler
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"error": "Token missing"}), 401
        
        try:
            parts = auth_header.split(" ")

            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({"error": "Invalid authorization header"}), 401
            token = parts[1]
            
            user = JwtHandler.decode_token(token)
            request.user = user
            
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    
    return decorated