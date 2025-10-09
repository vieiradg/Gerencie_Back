from src.model import db
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class userModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True)
    
    # CAMPOS DE PERFIL E CONTATO (CAUSA DO ERRO DE LOGIN)
    rg = Column(String(20), nullable=True, unique=True)
    phone_number = Column(String(20), nullable=True) 
    nationality = Column(String(50), nullable=True)
    marital_status = Column(String(50), nullable=True)
    profession = Column(String(100), nullable=True)

    street = Column(String(100), nullable=True)
    street_number = Column(String(10), nullable=True)
    postal_code = Column(String(10), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    properties = relationship(
        "propertyModel",
        backref="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    tenants = relationship(
        "tenantModel",
        backref="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    contracts = relationship(
        "contractModel",
        backref="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self) -> dict:
        full_address = f"{self.street or ''}, {self.street_number or ''}, CEP {self.postal_code or ''}"
        
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "rg": self.rg,
            "cpf": self.cpf,
            "phone_number": self.phone_number,
            "nationality": self.nationality,
            "marital_status": self.marital_status,
            "profession": self.profession,
            "address": full_address.strip(', CEP ') or 'Não Informado',
            "street": self.street,
            "street_number": self.street_number,
            "postal_code": self.postal_code,
        }