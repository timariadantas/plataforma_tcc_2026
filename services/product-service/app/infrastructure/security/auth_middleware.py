import time
from functools import wraps

import jwt
from flask import jsonify, request, g

from api.dto.response.api_response import ApiResponse
from infrastructure.security.jwt_handler import JwtHandler


def _authentication_error(error_message):
    elapsed = int(
        (time.perf_counter() - g.start_time) * 1000
    )

    response = ApiResponse(
        message="Request failed",
        elapsed=elapsed,
        error=error_message
    )

    return jsonify(response.to_dict()), 401


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return _authentication_error("Token missing")

        try:
            parts = auth_header.split(" ")

            if len(parts) != 2 or parts[0].lower() != "bearer":
                return _authentication_error(
                    "Invalid authorization header"
                )

            token = parts[1]

            user = JwtHandler.decode_token(token)
            request.user = user

        except jwt.ExpiredSignatureError:
            return _authentication_error("Token expired")

        except jwt.InvalidTokenError:
            return _authentication_error("Invalid token")

        return f(*args, **kwargs)

    return decorated