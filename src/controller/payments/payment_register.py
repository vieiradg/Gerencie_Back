from flask import request, jsonify
from flasgger.utils import swag_from
from . import bp_payment
from src.model.payment_model import paymentModel
from src.model.contract_model import contractModel
from src.model import db
from src.security.jwt_config import token_required
from sqlalchemy import and_
from datetime import datetime, timedelta

@bp_payment.route("/register", methods=["POST"])
@token_required
@swag_from("../../docs/payment_register.yml")
def register_payment(user_data):
     data = request.get_json()
     user_id = user_data["id"]

    # Verifica se o contrato existe
     contract = db.session.execute(
          db.select(contractModel).where(contractModel.id == data["contract_id"])
     ).scalar_one_or_none()

     if not contract:
        return jsonify({"message": "Contrato não encontrado"}), 404

    # Calcula a parcela baseada na data de início do contrato
     start_date = contract.start_date
     payment_date = datetime.strptime(data["payment_date"], "%Y-%m-%d").date()
     months_diff = (payment_date.year - start_date.year) * 12 + (payment_date.month - start_date.month) + 1

     lease_period = int(contract.lease_period)  # converte para inteiro
     if months_diff < 1 or months_diff > lease_period:
          return jsonify({"message": "Parcela inválida para o período do contrato"}), 400


     installment_number = months_diff

    # Verifica se já existe um pagamento para esta parcela
     payment_exists = db.session.execute(
        db.select(paymentModel).where(
            and_(
                paymentModel.contract_id == data["contract_id"],
                paymentModel.installment_number == installment_number
            )
        )
    ).scalar_one_or_none()

     if payment_exists:
        return jsonify({"message": f"Pagamento da parcela {installment_number} já registrado"}), 400

    # Define status automaticamente: paid se valor pago >= valor do aluguel
     status = "paid" if data["amount_paid"] >= contract.rent_value else "partial"

    # Cria o pagamento
     payment = paymentModel(
        contract_id=data["contract_id"],
        payment_date=payment_date,
        amount_paid=data["amount_paid"],
        installment_number=installment_number,
        total_installments=contract.lease_period,
        status=status
    )

     try:
        db.session.add(payment)
        db.session.commit()
        return jsonify({"message": "Pagamento registrado com sucesso", "payment": payment.to_dict()}), 201
     except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao registrar pagamento", "error": str(e)}), 500
