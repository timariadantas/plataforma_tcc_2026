from infrastructure.errors.service_errors import ValidationError


class ChangePasswordRequestDto:

    def __init__(self, new_password):
        self.new_password = new_password

    @staticmethod
    def from_dict(data):

        if not isinstance(data, dict):
            raise ValidationError("Request body must be a JSON object")

        new_password = data.get("new_password")

        if not new_password:
            raise ValidationError("new_password is required")

        if not isinstance(new_password, str):
            raise ValidationError("new_password must be a string")

        if len(new_password) < 4:
            raise ValidationError(
                "new_password must contain at least 4 characters"
            )

        return ChangePasswordRequestDto(
            new_password=new_password
        )