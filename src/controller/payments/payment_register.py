from flask import request, jsonify
from flasgger.utils import swag_from
from . import bp_payment
from src.model.payment_model import paymentModel
from src.model.contract_model import contractModel
from src.model import db
from src.security.jwt_config import token_required
from sqlalchemy import and_
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

@bp_payment.route("/register", methods=["POST"])
@token_required
@swag_from("../../docs/payment_register.yml")
def register_payment(user_data):
    data = request.get_json()

    # Verifica se o contrato existe
    contract = db.session.execute(
        db.select(contractModel).where(contractModel.id == data["contract_id"])
    ).scalar()

    if not contract:
        return jsonify({"message": "Contrato não encontrado"}), 404

    # Dados do contrato
    start_date = contract.start_date          # início do contrato
    lease_period = contract.lease_period      # duração em meses
    payment_date = datetime.strptime(data["payment_date"], "%Y-%m-%d").date()

    # --- Cálculo do número da parcela ---
    # quantos meses se passaram desde o início
    diff_months = (payment_date.year - start_date.year) * 12 + (payment_date.month - start_date.month)

    # primeira parcela é no mês seguinte
    installment_number = diff_months

    # se a data do pagamento for antes do start_date, parcela = 0
    if payment_date < start_date:
        installment_number = 0

    # garante que não ultrapasse o total de parcelas
    if installment_number > lease_period:
        installment_number = lease_period

    # Verifica se já existe um pagamento para esta parcela
    payment_exists = db.session.execute(
        db.select(paymentModel).where(
            and_(
                paymentModel.contract_id == data["contract_id"],
                paymentModel.installment_number == installment_number
            )
        )
    ).scalar()

    if payment_exists:
        return jsonify({"message": f"Pagamento da parcela {installment_number} já registrado"}), 400

    # Define status automaticamente
    status = "paid" if data["amount_paid"] >= contract.rent_value else "partial"

    # Cria o pagamento
    payment = paymentModel(
        contract_id=data["contract_id"],
        payment_date=payment_date,
        amount_paid=data["amount_paid"],
        installment_number=installment_number,
        total_installments=lease_period,
        status=status
    )

    try:
        db.session.add(payment)
        db.session.commit()
        return jsonify({
            "message": "Pagamento registrado com sucesso",
            "payment": payment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao registrar pagamento", "error": str(e)}), 500
