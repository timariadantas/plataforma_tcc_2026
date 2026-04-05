class ClientResponseDto:
    def __init__(self, id, name, surname, email):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        
    @staticmethod
    def from_entity(client):
        return ClientResponseDto(
        id= str(client.id),
        name = client.name,
        surname = client.surname,
        email= client.email
    )
    def to_dict(self):
        return{
            "id" : self.id,
            "name" : self.name,
            "surname" : self.surname,
            "email": self.email
        }