from app.infrastructure.security.jwt_handler import JwtHandler

token = JwtHandler.generate_token({"user": "admin"})
print(token)