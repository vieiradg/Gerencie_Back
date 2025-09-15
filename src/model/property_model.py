from src.model import db
from sqlalchemy.schema import Column
from sqlalchemy import Column, Integer, String, ForeignKey

class propertyModel(db.Model):
    __tablename__ = 'properties'

    # campos obrigatorios de cadfastro
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    house_name = Column(String(25), nullable=True )

    postal_code = Column(String(10), nullable=False)
    house_number = Column(String(10), nullable=False)
    house_complement = Column(String(50), nullable=True)


    def to_dict(self) -> dict:
        return {
            "id": self.id, "user_id": self.user_id,
            "house_number": self.house_number,
            "house_complement": self.house_complement,
            "postal_code": self.postal_code,
            "house_name": self.house_name
            }