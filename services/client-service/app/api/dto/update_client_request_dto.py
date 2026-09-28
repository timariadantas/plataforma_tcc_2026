from datetime import datetime

from infrastructure.errors.service_errors import ValidationError


class UpdateClientRequestDto:

    def __init__(
        self,
        name,
        surname,
        email,
        
    ):
        self.name = name
        self.surname = surname
        self.email = email
        

    @staticmethod
    def from_dict(data):

        if not isinstance(data, dict):
            raise ValidationError(
                "Request body must be a JSON object"
            )

        name = data.get("name")
        surname = data.get("surname")
        email = data.get("email")
      

        if not name:
            raise ValidationError("name is required")

        if not surname:
            raise ValidationError("surname is required")

        if not email:
            raise ValidationError("email is required")

        if not isinstance(name, str):
            raise ValidationError("name must be a string")

        if not isinstance(surname, str):
            raise ValidationError("surname must be a string")

        if not isinstance(email, str):
            raise ValidationError("email must be a string")

        return UpdateClientRequestDto(
            name=name,
            surname=surname,
            email=email,
         
        )