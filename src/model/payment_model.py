from src.model import db
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date

class paymentModel(db.Model):
    __tablename__ = 'payments'  # nome da tabela no banco de dados

    # Campos do pagamento
    id = Column(Integer, primary_key=True, autoincrement=True)  # id do pagamento
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)  # id do contrato associado
    # adjustment_id = Column(Integer, ForeignKey("adjustments.id"), nullable=True)  # id do reajuste, se houver
    payment_date = Column(Date, nullable=False)  # data do pagamento
    amount_paid = Column(Float, nullable=False)  # valor pago
    status = Column(String(20), nullable=False, default="pending")  # status do pagamento (pending, paid, late etc.)

    # Novas colunas para controle de parcelas
    installment_number = Column(Integer, nullable=False)  # número da parcela
    total_installments = Column(Integer, nullable=False)  # total de parcelas do contrato

    # Método para converter o objeto em dicionário
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            # "adjustment_id": self.adjustment_id,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "amount_paid": self.amount_paid,
            "status": self.status,
            "installment_number": self.installment_number,
            "total_installments": self.total_installments
        }
