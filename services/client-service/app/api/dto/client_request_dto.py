from datetime import datetime

from infrastructure.errors.service_errors import ValidationError


class CreateClientRequestDto:

    def __init__(
        self,
        name,
        surname,
        email,
        password,
        birthdate
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.birthdate = birthdate

    @staticmethod
    def from_dict(data):

        if not isinstance(data, dict):
            raise ValidationError(
                "Request body must be a JSON object"
            )

        name = data.get("name")
        surname = data.get("surname")
        email = data.get("email")
        password = data.get("password")
        birthdate_value = data.get("birthdate")

        if not name:
            raise ValidationError("name is required")

        if not surname:
            raise ValidationError("surname is required")

        if not email:
            raise ValidationError("email is required")

        if not password:
            raise ValidationError("password is required")

        if not birthdate_value:
            raise ValidationError("birthdate is required")

        if not isinstance(name, str):
            raise ValidationError("name must be a string")

        if not isinstance(surname, str):
            raise ValidationError("surname must be a string")

        if not isinstance(email, str):
            raise ValidationError("email must be a string")

        if not isinstance(password, str):
            raise ValidationError("password must be a string")

        if not isinstance(birthdate_value, str):
            raise ValidationError(
                "birthdate must be a string"
            )

        try:
            birthdate = datetime.strptime(
            birthdate_value,
            "%Y-%m-%d"
            ).date()

        except ValueError as e:
            raise ValidationError("birthdate must be in YYYY-MM-DD format") from e

        return CreateClientRequestDto(
                    name=name,
                    surname=surname,
                    email=email,
                    password=password,
                    birthdate=birthdate
            )