from flask import jsonify
# from flasgger.utils import swag_from
from . import bp_dashboard
from src.model.property_model import propertyModel
from src.model.contract_model import contractModel
from src.model.tenant_model import tenantModel
from src.model import db
from src.security.jwt_config import token_required

@bp_dashboard.route("/properties_panel", methods=["GET"])
@token_required
def property_panel(user_data):
    try:
     
        properties = db.session.execute(
        db.select(propertyModel).where(propertyModel.user_id == user_data["id"])
        ).scalars().all()

        propertys_list = []

        for property in properties:
            property_dict = property.to_dict()

            contract_data = db.session.execute(
                db.select(contractModel.id, contractModel.status)
                .where(contractModel.property_id == property.id)
            ).first()

            if contract_data:
                property_dict["contract"] = {"id": contract_data.id, "status": contract_data.status}
            else:
                property_dict["contract"] = None

            propertys_list.append(property_dict)

        return jsonify({"properties": propertys_list})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500