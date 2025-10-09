from src.model import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class tenantModel(db.Model):
    __tablename__ = 'tenants'
    __table_args__ = (
        UniqueConstraint('user_id', 'cpf', name='uq_user_cpf'),
        UniqueConstraint('user_id', 'phone_number', name='uq_user_phone'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String(120), nullable=False)
    phone_number = Column(String(20), nullable=False) 
    cpf = Column(String(14), nullable=False)
    
    # CAMPOS DE PERFIL E CONTATO
    email = Column(String(120), nullable=True)
    nationality = Column(String(50), nullable=True)
    marital_status = Column(String(50), nullable=True)
    profession = Column(String(100), nullable=True)
    
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="SET NULL"), nullable=True)
    
    status = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    property = relationship("propertyModel", backref="tenants")

    contracts = relationship(
        "contractModel", backref="tenant", cascade="all, delete-orphan", passive_deletes=True
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "cpf": self.cpf,
            "phone_number": self.phone_number,
            "email": self.email,
            "nationality": self.nationality,
            "marital_status": self.marital_status,
            "profession": self.profession,
            "status": self.status,
            "property_id": self.property_id
        }