from src.model import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class tenantModel(db.Model):
    __tablename__ = 'tenants'
    __table_args__ = (
        UniqueConstraint('user_id', 'cpf', name='uq_user_cpf'),
        UniqueConstraint('user_id', 'phone_number', name='uq_user_phone'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False)
    phone_number = Column(String(11), nullable=False)
    status = Column(Integer, nullable=False, default=0)

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
            "status": self.status
        }
