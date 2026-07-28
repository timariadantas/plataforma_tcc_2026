from flask import request, jsonify
from functools import wraps
from infrastructure.security.jwt_handler import JwtHandler

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"error": "Invalid token"}), 401
        
        try:
            token = auth_header.split(" ")[1]
            user = JwtHandler.decode_token(token)
            request.user = user
        except Exception:
            return jsonify ({"error" : "Invalid token"}), 401
        
        return f(*args, **kwargs)
    
    return decorated