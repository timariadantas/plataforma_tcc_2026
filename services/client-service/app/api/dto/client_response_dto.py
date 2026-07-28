class ClientResponseDto:
    def __init__(self, client):
        self.id = client.id
        self.name = client.name
        self.surname = client.surname
        self.email = client.email
        self.birthdate = client.birthdate
        self.active = client.active
        self.created_at = client.created_at
        self.updated_at = client.updated_at
        
    @staticmethod
    def from_entity(client):
        return ClientResponseDto(client)

    def to_dict(self):
        return {
  
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "birthdate": self.birthdate.isoformat() if self.birthdate else None,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }