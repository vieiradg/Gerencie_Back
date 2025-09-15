from src.model import db
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date

class paymentModel(db.Model):
    __tablename__ = 'payments'  # nome da tabela no banco de dados

    # Campos do pagamento
    id = Column(Integer, primary_key=True, autoincrement=True)  
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)  
    payment_date = Column(Date, nullable=False)  
    amount_paid = Column(Float, nullable=False)  
    installment_number = Column(Integer, nullable=False)  # número da parcela
    total_installments = Column(Integer, nullable=False)  # total de parcelas do contrato

    # Novas colunas para controle de parcelas



    status = Column(String(20), nullable=False, default="pending")  

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "amount_paid": self.amount_paid,
            "status": self.status,
            "installment_number": self.installment_number,
            "total_installments": self.total_installments
        }
