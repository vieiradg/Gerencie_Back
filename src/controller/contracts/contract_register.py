from flask import request, jsonify
from sqlalchemy import and_
from flasgger.utils import swag_from
from . import bp_contract
from src.model.contract_model import contractModel
from src.model.payment_model import paymentModel
from src.model.property_model import propertyModel
from src.model import db
from src.security.jwt_config import token_required
from dateutil.relativedelta import relativedelta
from datetime import datetime

@bp_contract.route("/register", methods=["POST"])
@token_required
def register(user_data):
    data = request.get_json()
    user_id = user_data["id"]

    # Verifica se o imóvel existe
    property_exists = db.session.get(propertyModel, data["property_id"])
    if not property_exists:
        return jsonify({"message": "Imóvel não encontrado"}), 404

    # Verifica se já existe contrato para o mesmo inquilino e imóvel
    contract_exists = db.session.execute(
        db.select(contractModel).where(
            and_(
                contractModel.tenant_id == data["tenant_id"],
                contractModel.property_id == data["property_id"],
            )
        )
    ).scalar_one_or_none()

    if contract_exists:
        return jsonify({"message": "Inquilino já possui contrato nesse imóvel"}), 400

    # Cria o contrato
    contract = contractModel(
        user_id=user_id,
        tenant_id=data["tenant_id"],
        property_id=data["property_id"],
        lease_period=data["lease_period"],
        rent_value=data["rent_value"],
        due_day=data["due_day"],
        start_date=data["start_date"]
    )

    try:
        db.session.add(contract)
        db.session.commit()

        # Gera as parcelas
        start_date = contract.start_date
        total_months = contract.lease_period
        for i in range(total_months):
            vencimento = start_date + relativedelta(months=i)
            parcela = paymentModel(
                contract_id=contract.id,
                installment_number=i+1,
                amount_paid=None,
                status="pending",
                payment_date=vencimento
            )
            db.session.add(parcela)

        db.session.commit()

        # Busca todas as parcelas geradas
        parcelas = db.session.execute(
            db.select(paymentModel).where(paymentModel.contract_id == contract.id)
        ).scalars().all()

        # Monta o JSON de retorno

        return jsonify({
            "message": "Contrato cadastrado com sucesso e parcelas geradas"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao cadastrar contrato", "error": str(e)}), 500
