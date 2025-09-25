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

    # campos posteriores de cadastro
    rg = Column(String(20), nullable=True, unique=True)
    street = Column(String(100), nullable=True)
    street_number = Column(String(10), nullable=True)
    postal_code = Column(String(10), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "rg": self.rg,
            "cpf": self.cpf,
            "street": self.street,
            "street_number": self.street_number,
            "postal_code": self.postal_code
            }