from datetime import datetime
import uuid

class Client:
    def __init__(self, name:str, surname:str, email:str, birthdate:datetime):
        self._validate(name, surname, email, birthdate)
        self.id = str(uuid.uuid4())
        self.name = name
        self.surname = surname
        self.email = email
        self.birthdate = birthdate
        self.active = True
        
        now = datetime.now()
        self.created_at = now
        self.updated_at = now
        
# Validações do dominio
    def _validate(self, name, surname, email, birthdate):
        if not name or not name.strip():
            raise ValueError("Nome é Obrigatório")
        if not surname or not surname.strip():
            raise ValueError("Sobrenome é obrigatório")
        if not email or "@" not in email:
            raise ValueError("Email inválido")
        if not isinstance(birthdate, datetime):
            raise ValueError("Data de nascimento inválida")
    
# Comportamento de atualização e delete(lógico)
    def update(self, name:str, surname:str, email:str):
        self._validate(name, surname, email, self.birthdate)
        self.name = name
        self.surname = surname
        self.email = email
        self.updated_at = datetime.now()
        
    def disabled(self):
        if not self.active:
            raise ValueError("Cliente desativado")
        
        self.active = False
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "birthdate": str(self.birthdate),
            "active": self.active,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
    }
        




    