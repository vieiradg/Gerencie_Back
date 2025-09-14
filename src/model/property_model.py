from src.model import db
from sqlalchemy.schema import Column
from sqlalchemy import Column, Integer, String, ForeignKey

class propertyModel(db.Model):
    __tablename__ = 'propertys'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    house_street = Column(String(100), nullable=False)
    house_number = Column(String(10), nullable=False)
    house_complement = Column(String(50), nullable=True)
    city = Column(String(50), nullable=False)
    house_neighborhood = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=False)
    
    
    def to_dict(self) -> dict:
        return {
            "id": self.id, "user_id": self.user_id,
            "house_street": self.house_street,
            "house_number": self.house_number,
            "house_complement": self.house_complement,
            "city": self.city,
            "house_neighborhood": self.house_neighborhood,
            "postal_code": self.postal_code
            }