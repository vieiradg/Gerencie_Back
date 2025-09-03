from src.model import db
from sqlalchemy.schema import Column
from sqlalchemy import Column, Integer, String, ForeignKey

class contractModel(db.Model):
    __tablename__ = 'contracts'

    # campos obrigatorios de cadfastro
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    poperty_id = Column(Integer, ForeignKey("propertys.id"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    adjustment_id = Column(Integer, ForeignKey("readjustments.id"), nullable=False)
    house_street = Column(String(100), nullable=False)
    house_number = Column(String(10), nullable=False)
    house_complement = Column(String(50), nullable=True)
    city = Column(String(50), nullable=False)
    postal_code = Column(String(10), nullable=False)
    lease_period = Column(String(3), nullable=False)
    rent_value = Column(String(20), nullable=False)
    due_day = Column(String(2), nullable=False)
    start_date = Column(String(10), nullable=False)



    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "poperty_id": self.poperty_id,
            "payment_id": self.payment_id,
            "adjustment_id": self.adjustment_id,
            "house_street": self.house_street,
            "house_number": self.house_number,
            "house_complement": self.house_complement,
            "city": self.city,
            "postal_code": self.postal_code,
            "lease_period": self.lease_period,
            "rent_value": self.rent_value,
            "due_day": self.due_day,
            "start_date": self.start_date

            }