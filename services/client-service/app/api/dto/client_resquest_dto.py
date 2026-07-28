from datetime import datetime


class ClientRequestDto:

    def __init__(self, name, surname, email, password, birthdate):
        self.name = name
        self.surname = surname
        self.email = email
        self.password= password
        self.birthdate = birthdate

    @staticmethod
    def from_dict(data):

        birthdate = datetime.strptime(
            data.get("birthdate"),
            "%Y-%m-%d"
        ).date()

        return ClientRequestDto(
            name=data.get("name"),
            surname=data.get("surname"),
            email=data.get("email"),
            password=data.get("password"),
            birthdate=birthdate
        )