from src.model import db
from sqlalchemy import Column, Integer, String, ForeignKey

class tenantModel(db.Model):
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    phone_number = Column(String(11), nullable=False, unique=True)
    status = Column(Integer, nullable=False, default=0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "status": self.status
        }
