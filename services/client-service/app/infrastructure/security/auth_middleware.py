from flask import request
from functools import wraps
from infrastructure.security.jwt_handler import JwtHandler
from infrastructure.errors.service_errors import ( AuthenticationError )

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            raise AuthenticationError("Authentication required" )

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationError( "Invalid token" )

        token = parts[1]

        try:
            user = JwtHandler.decode_token(token)
            request.user = user

        except Exception:
            raise AuthenticationError ( "Invalid token" )
        
        return f(*args, **kwargs)

    return decorated
        
        