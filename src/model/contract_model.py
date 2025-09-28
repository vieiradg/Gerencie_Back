from src.model import db
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class contractModel(db.Model):
    __tablename__ = "contracts"

    # Campos obrigatórios de cadastro
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    lease_period = Column(Integer, nullable=False)  # agora inteiro (meses)
    rent_value = Column(Float, nullable=False)  # valor do aluguel como float
    due_day = Column(Integer, nullable=False)  # dia do vencimento como inteiro
    start_date = Column(Date, nullable=False)
    status = Column(Integer, nullable=False, default=0)

    payments = relationship(
    "paymentModel", backref="contract", cascade="all, delete-orphan", passive_deletes=True
)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "property_id": self.property_id,
            "lease_period": self.lease_period,
            "rent_value": self.rent_value,
            "due_day": self.due_day,
            "start_date": (
                self.start_date.strftime("%d/%m/%Y") if self.start_date else None
            ),
            "status": self.status,
        }
