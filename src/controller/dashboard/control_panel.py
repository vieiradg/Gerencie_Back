from flask import request, jsonify
from sqlalchemy import and_, extract, func
from . import bp_dashboard
from src.model.user_model import userModel
from src.model.tenant_model import tenantModel
from src.model.property_model import propertyModel
from src.model.contract_model import contractModel
from src.model.payment_model import paymentModel
from src.model import db
from src.security.jwt_config import token_required
from datetime import date
from collections import defaultdict

@bp_dashboard.route("/control_panel", methods=["GET"])
@token_required
def control_panel(user_data):
    try:
        today = date.today()

        results = db.session.execute(
            db.select(
                contractModel,
                tenantModel,
                propertyModel,
                paymentModel
            )
            .join(tenantModel, tenantModel.id == contractModel.tenant_id)
            .join(propertyModel, propertyModel.id == contractModel.property_id)
            .join(paymentModel, paymentModel.contract_id == contractModel.id, isouter=True)
            .where(contractModel.user_id == user_data["id"])
        ).all()
        
        # Inicializa métricas
        active_tenants = set()   # uso set() para evitar duplicados
        pending_rents = 0
        total_receive_month = 0.0

        for contract, tenant, property_, payment in results:
            # Conta inquilinos ativos
            if tenant.status == 0:
                active_tenants.add(tenant.id)

            # Conta (ou melhor: soma) aluguéis pendentes (data vencida ou hoje e status = pending)
            if payment and payment.status == "pending" and payment.payment_date <= today:
                pending_rents += contract.rent_value   # soma o valor em dinheiro

            # Soma total recebido no mês atual
            if payment and payment.status == "paid":
                if payment.payment_date and payment.payment_date.month == today.month and payment.payment_date.year == today.year:
                    total_receive_month += payment.amount_paid or 0

        response = {
            "active_tenants": len(active_tenants),
            "pending_rents": pending_rents,
            "total_receive_month": total_receive_month
        }

        return jsonify(response), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
