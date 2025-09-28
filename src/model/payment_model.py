from src.model import db
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date

class paymentModel(db.Model):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False) 
    payment_date = Column(Date, nullable=True)
    installment_number = Column(Integer, nullable=False)  
    amount_paid = Column(Float, nullable=True)  
    adjustment_date = Column(Date, nullable=True)  
    previous_amount = Column(Float, nullable=True)  
    new_amount = Column(Float, nullable=True)  
    reason_for_adjustment = Column(String(255), nullable=True)  
    status = Column(String(20), nullable=False, default="pending")  

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "installment_number": self.installment_number,
            "amount_paid": self.amount_paid,
            "adjustment_date": self.adjustment_date.isoformat() if self.adjustment_date else None,
            "previous_amount": self.previous_amount,
            "new_amount": self.new_amount,
            "reason_for_adjustment": self.reason_for_adjustment,
            "status": self.status,
    }
