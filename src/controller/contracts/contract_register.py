from flask import request, jsonify
from sqlalchemy import and_
from flasgger.utils import swag_from
from . import bp_contract
from src.model.contract_model import contractModel
from src.model.payment_model import paymentModel
from src.model.property_model import propertyModel
from src.model.tenant_model import tenantModel
from src.model import db
from src.security.jwt_config import token_required
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

def calculate_lease_period(start_date, end_date):
    diff = relativedelta(end_date, start_date)
    total_months = diff.years * 12 + diff.months
    if diff.days > 0 or diff.microseconds > 0:
        total_months += 1
    return total_months

@bp_contract.route("/register", methods=["POST"])
@token_required
def register(user_data):
    data = request.get_json()
    user_id = user_data["id"]

    required_fields = ["tenant_id", "property_id", "rent_value", "due_day", "start_date", "end_date"]
    for field in required_fields:
        if not data.get(field):
             return jsonify({"message": f"O campo '{field}' é obrigatório."}), 400

    property_exists = db.session.get(propertyModel, data["property_id"])
    if not property_exists:
        return jsonify({"message": "Imóvel ou Inquilino não encontrado"}), 404

    contract_exists = contractModel.query.filter_by(
        tenant_id=data["tenant_id"], 
        property_id=data["property_id"]
    ).first()

    if contract_exists:
        return jsonify({"message": "Inquilino já possui contrato nesse imóvel"}), 400

    try:
        start_date_obj = datetime.strptime(data["start_date"], '%Y-%m-%d')
        end_date_obj = datetime.strptime(data["end_date"], '%Y-%m-%d')
        
        if end_date_obj <= start_date_obj:
            return jsonify({"message": "A data de término deve ser posterior à data de início."}), 400

        lease_period_months = calculate_lease_period(start_date_obj, end_date_obj)

    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use YYYY-MM-DD."}), 400
    
    contract = contractModel(
        user_id=user_id,
        tenant_id=data["tenant_id"],
        property_id=data["property_id"],
        lease_period=lease_period_months,
        rent_value=data["rent_value"],
        due_day=data["due_day"],
        start_date=start_date_obj.date(),
        end_date=end_date_obj.date(),
    )

    try:
        db.session.add(contract)
        db.session.commit()
        
        for i in range(contract.lease_period):
            vencimento_base = start_date_obj + relativedelta(months=i)
            
            try:
                vencimento = datetime(vencimento_base.year, vencimento_base.month, contract.due_day)
            except ValueError:
                vencimento = datetime(vencimento_base.year, vencimento_base.month + 1, 1) - timedelta(days=1)

            parcela = paymentModel(
                contract_id=contract.id,
                installment_number=i+1,
                amount_paid=None,
                status="pending",
                payment_date=vencimento.date()
            )
            db.session.add(parcela)

        db.session.commit()
        
        return (
            jsonify(
                {
                    "message": "Contrato cadastrado com sucesso e parcelas geradas",
                    "contract": contract.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao cadastrar contrato", "error": str(e)}), 500


@bp_contract.route("/delete/<int:contract_id>", methods=["DELETE"])
@token_required
def delete_contract(user_data, contract_id):
    user_id = user_data["id"]

    try:
        contract_to_delete = contractModel.query.filter(
            contractModel.id == contract_id,
            contractModel.user_id == user_id
        ).first()

        if not contract_to_delete:
            return jsonify({"message": "Contrato não encontrado ou não autorizado."}), 404

        db.session.delete(contract_to_delete)
        db.session.commit()

        return jsonify({"message": "Contrato excluído com sucesso."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao excluir contrato", "error": str(e)}), 500


@bp_contract.route("/contract/<int:contract_id>", methods=["GET"])
@token_required
def get_contract_details(user_data, contract_id):
    user_id = user_data["id"]

    try:
        contract = contractModel.query.filter_by(
            id=contract_id, user_id=user_id
        ).first()

        if not contract:
            return jsonify({"message": "Contrato não encontrado ou não autorizado."}), 404

        return jsonify(contract.to_dict()), 200

    except Exception as e:
        return jsonify({"message": "Erro ao buscar detalhes do contrato", "error": str(e)}), 500


@bp_contract.route("/update/<int:contract_id>", methods=["PUT"])
@token_required
def update_contract(user_data, contract_id):
    user_id = user_data["id"]
    data = request.get_json()

    try:
        contract_to_update = contractModel.query.filter_by(
            id=contract_id, user_id=user_id
        ).first()

        if not contract_to_update:
            return jsonify({"message": "Contrato não encontrado ou não autorizado."}), 404
        
        if 'status' in data:
             contract_to_update.status = data['status']

        db.session.commit()

        return jsonify({"message": "Contrato atualizado com sucesso.", "contract": contract_to_update.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar contrato", "error": str(e)}), 500