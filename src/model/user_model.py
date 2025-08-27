from src.model import db
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer


class userModel(db.Model):
    __tablename__ = 'users'

    # campos obrigatorios de cadfastro
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    
    # campos para cadastro complementar
    occupation = Column(String(50), nullable=True)
    marital_status = Column(String(20), nullable=True)
    postal_code = Column(String(10), nullable=True)
    house_number = Column(String(10), nullable=True)
    rg = Column(String(20), nullable=True, unique=True)
    
    def to_dict(self) -> dict:
        return {"id": self.id}