from flask import request, jsonify
from flasgger.utils import swag_from
from . import bp_payment
from src.model.payment_model import paymentModel
from src.model.contract_model import contractModel
from src.model import db
from src.security.jwt_config import token_required
from sqlalchemy import and_
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from src.model.property_model import propertyModel


@bp_payment.route("/register", methods=["POST"])
@token_required
@swag_from("../../docs/payment_register.yml")
def register_payment(user_data):
    data = request.get_json()
    user_id = user_data["id"]

    required_fields = ["contract_id", "payment_date", "amount_paid"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"O campo '{field}' é obrigatório."}), 400

    try:
        contract = db.session.execute(
            db.select(contractModel).where(contractModel.id == data["contract_id"])
        ).scalar()

        if not contract:
            return jsonify({"message": "Contrato não encontrado"}), 404
        
        start_date = contract.start_date
        lease_period = contract.lease_period
        
        payment_date_obj = datetime.strptime(data["payment_date"], "%Y-%m-%d").date()
        amount_paid = data["amount_paid"]
        
        diff = relativedelta(payment_date_obj, start_date)
        diff_months = diff.years * 12 + diff.months

        installment_number = diff_months + 1 

        if payment_date_obj < start_date:
             return jsonify({"message": "Data de pagamento anterior à data de início do contrato."}), 400

        if installment_number > lease_period:
            return jsonify({"message": f"Parcela {installment_number} excede a duração do contrato ({lease_period} parcelas)."}), 400

        payment_exists = db.session.execute(
            db.select(paymentModel).where(
                and_(
                    paymentModel.contract_id == data["contract_id"],
                    paymentModel.installment_number == installment_number
                )
            )
        ).scalar()

        if payment_exists:
            return jsonify({"message": f"Pagamento da parcela {installment_number} já registrado."}), 400

        status = "paid" if amount_paid >= contract.rent_value else "partial"

        payment = paymentModel(
            contract_id=data["contract_id"],
            payment_date=payment_date_obj,
            amount_paid=amount_paid,
            installment_number=installment_number,
            total_installments=lease_period,
            status=status
        )

        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            "message": "Pagamento registrado com sucesso",
            "payment": payment.to_dict()
        }), 201
        
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use YYYY-MM-DD."}), 400
    except Exception as e:
        db.session.rollback()
        print(f"ERRO CRÍTICO NO REGISTRO DE PAGAMENTO: {e}")
        return jsonify({"message": "Erro ao registrar pagamento", "error": str(e)}), 500


@bp_payment.route("/list", methods=["GET"])
@token_required
def list_payments(user_data):
    user_id = user_data["id"]
    current_date = date.today()

    try:
        payments_query = db.session.query(
            paymentModel,
            contractModel,
            propertyModel.house_name,
            propertyModel.house_number
        ).join(
            contractModel, paymentModel.contract_id == contractModel.id
        ).outerjoin(
            propertyModel, contractModel.property_id == propertyModel.id
        ).filter(
            contractModel.user_id == user_id
        ).all()

        payments_list = []
        for payment, contract, house_name, house_number in payments_query:
            payment_dict = payment.to_dict()
            
            effective_status = payment_dict['status']
            if effective_status == 'pending' and payment.payment_date < current_date:
                effective_status = 'overdue'

            property_display_name = f"{house_name}, {house_number}" if house_name else 'Imóvel N/A'
            
            payment_dict['contract_id'] = contract.id
            payment_dict['amount'] = contract.rent_value 
            payment_dict['property_name'] = property_display_name
            payment_dict['status'] = effective_status
            
            payments_list.append(payment_dict)

        return jsonify({"payments": payments_list}), 200

    except Exception as e:
        print(f"ERRO CRÍTICO AO LISTAR PAGAMENTOS: {e}")
        return jsonify({"error": "Erro interno ao carregar pagamentos", "details": str(e)}), 500


@bp_payment.route("/status/<int:payment_id>", methods=["PUT"])
@token_required
def update_payment_status(user_data, payment_id):
    user_id = user_data["id"]
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["paid", "pending", "partial", "overdue"]:
        return jsonify({"message": "Status inválido fornecido."}), 400

    try:
        payment_to_update = db.session.query(paymentModel).join(
            contractModel, paymentModel.contract_id == contractModel.id
        ).filter(
            paymentModel.id == payment_id,
            contractModel.user_id == user_id
        ).first()

        if not payment_to_update:
            return jsonify({"message": "Pagamento não encontrado ou não autorizado."}), 404

        payment_to_update.status = new_status
        
        if new_status == "paid":
             rent_value = contractModel.query.filter_by(id=payment_to_update.contract_id).first().rent_value
             
             payment_to_update.amount_paid = rent_value
             payment_to_update.payment_date = date.today()
        
        db.session.commit()
        
        return jsonify({"message": "Status de pagamento atualizado com sucesso."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"ERRO CRÍTICO AO ATUALIZAR STATUS: {e}")
        return jsonify({"error": "Erro interno ao atualizar status", "details": str(e)}), 500