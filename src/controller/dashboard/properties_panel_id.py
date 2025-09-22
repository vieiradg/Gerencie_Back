from flask import jsonify
# from flasgger.utils import swag_from
from . import bp_dashboard
from src.model.property_model import propertyModel
from src.model.contract_model import contractModel
from src.model.tenant_model import tenantModel
from src.model import db
from src.security.jwt_config import token_required

@bp_dashboard.route("/properties_panel/<int:property_id>", methods=["GET"])
@token_required
def property_panel_id(user_data, property_id):
    try:
        # Buscar o imóvel específico do usuário
        property_item = db.session.execute(
            db.select(propertyModel)
            .where(propertyModel.user_id == user_data["id"])
            .where(propertyModel.id == property_id)
        ).scalar_one_or_none()  # retorna None se não existir

        if not property_item:
            return jsonify({"error": "Imóvel não encontrado"}), 404

        property_dict = property_item.to_dict()

        # Buscar contrato relacionado (objeto completo)
        contract_item = db.session.execute(
            db.select(contractModel)
            .where(contractModel.property_id == property_item.id)
        ).scalar_one_or_none()  # retorna None se não houver contrato

        contract_dict = contract_item.to_dict() if contract_item else None

        # Buscar inquilino somente se houver contrato
        tenant_dict = None
        if contract_item:
            tenant_item = db.session.execute(
                db.select(tenantModel)
                .where(tenantModel.id == contract_item.tenant_id)
            ).scalar_one_or_none()
            tenant_dict = tenant_item.to_dict() if tenant_item else None

        return jsonify({
            "property": property_dict,
            "contract": contract_dict,
            "tenant": tenant_dict
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

    