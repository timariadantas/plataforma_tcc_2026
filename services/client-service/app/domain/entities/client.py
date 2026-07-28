from datetime import datetime , date , timezone
import uuid
from infrastructure.errors.service_errors import ValidationError

class Client:
    def __init__(self, name:str, surname:str, email:str,password_hash: str, birthdate:date):
        self._validate(name, surname, email, password_hash, birthdate)
        self.id = str(uuid.uuid4())
        self.name = name
        self.surname = surname
        self.email = email
        self.password_hash = password_hash
        self.birthdate = birthdate
        self.active = True
        
        now = datetime.now((timezone.utc))
        self.created_at = now
        self.updated_at = now
        
# Validações do dominio
    def _validate(self, name, surname, email, password_hash,birthdate):
        if not name or not name.strip():
            raise ValidationError("Nome é Obrigatório")
        if not surname or not surname.strip():
            raise ValidationError("Sobrenome é obrigatório")
        if not email or "@" not in email:
            raise ValidationError("Email inválido")
        if not password_hash or len(password_hash) < 4:
            raise ValidationError("Senha inválida")
        if not isinstance(birthdate, date):
            raise ValidationError("Data de nascimento inválida")
    
# Comportamento de atualização e delete(lógico)
    def update(self, name:str, surname:str, email:str):
        self._validate(name, surname, email,self.password_hash, self.birthdate)
        self.name = name
        self.surname = surname
        self.email = email
        self.updated_at = datetime.now(timezone.utc)
        
    def disable(self):
        if not self.active:
            raise ValidationError("Cliente desativado")
        
        self.active = False
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "birthdate": self.birthdate.isoformat(),
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
    }
        




    