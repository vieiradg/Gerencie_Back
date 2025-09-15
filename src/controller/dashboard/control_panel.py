from flask import request, jsonify  # Importa módulos do Flask
from sqlalchemy import and_
from flasgger.utils import swag_from
from . import bp_dashboard

from src.model.user_model import userModel
from src.model.tenant_model import tenantModel
from src.model.property_model import propertyModel
from src.model import db
from src.security.jwt_config import token_required

@bp_dashboard.route("/control_panel", methods=["GET"])
@token_required
def control_panel(user_data):
    
    user = db.session.execute(
        db.select(userModel).where(userModel.id == user_data["id"])
    ).scalar()

    tenants = db.session.execute(
        db.select(tenantModel).where(
            and_(
                    tenantModel.user_id == user_data["id"],
                    tenantModel.status == 0
                ))
    ).scalars().all()
    
    properties = db.session.execute(
        db.select(propertyModel).where(propertyModel.user_id == user_data["id"])
    ).scalars().all()
    propertys_list = [property.to_dict() for property in properties]

    active_tenants = len(tenants) #ver os inquilinos ativos
    pending_rents = "" #ver os pagamentos que ainda faltam ser pagos
    total_received = "" #ver os pagamentos efetuados no mes
    contracts_to_expire = ""
    try:
        return jsonify({
        "user": user.to_dict(),
        "active_tenants": active_tenants,
        # "properties": propertys_list
    })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
