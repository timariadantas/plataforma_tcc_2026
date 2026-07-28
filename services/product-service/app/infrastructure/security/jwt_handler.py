import jwt
from datetime import datetime, timedelta, timezone

from infrastructure.security.jwt_config import JWT_SECRET, JWT_ALGORITHM


class JwtHandler:

    @staticmethod
    def generate_token(payload: dict, expires_minutes: int = 60):

        data = payload.copy()

        data["exp"] = datetime.now(timezone.utc) + timedelta(
            minutes=expires_minutes
        )

        return jwt.encode(
            data,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )


    @staticmethod
    def decode_token(token: str):

        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )