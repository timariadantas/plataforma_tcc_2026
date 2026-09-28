from infrastructure.errors.service_errors import ValidationError


class LoginRequestDto:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def from_dict(data):

        if not isinstance(data, dict):
            raise ValidationError(
                "Request body must be a JSON object"
            )

        email = data.get("email")
        password = data.get("password")

        if not email:
            raise ValidationError(
                "email is required"
            )

        if not password:
            raise ValidationError(
                "password is required"
            )

        if not isinstance(email, str):
            raise ValidationError(
                "email must be a string"
            )

        if not isinstance(password, str):
            raise ValidationError(
                "password must be a string"
            )

        return LoginRequestDto(
            email=email,
            password=password
        )