from datetime import datetime

class ClientRequestDto:
    def __init__(self, name, surname, email, birthdate):
        self.name = name
        self.surname = surname
        self.email = email
        self.birthdate = birthdate
        
    @staticmethod
    def from_dict(data):
        return ClientRequestDto(
            name=data.get("name"),
            surname=data.get("surname"),
            email=data.get("email"),
            birthdate=datetime.strptime(data.get("birthdate"), "%Y-%m-%d")
        )
        








