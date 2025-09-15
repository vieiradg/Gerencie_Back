from flask import jsonify
# from flasgger.utils import swag_from
from . import bp_dashboard
from src.model.property_model import propertyModel
from src.model.contract_model import contractModel
from src.model.tenant_model import tenantModel
from src.model import db
from src.security.jwt_config import token_required

@bp_dashboard.route("/tenants_panel", methods=["GET"])
@token_required
def tenants_panel(user_data):
    try:
        # JOIN tenant + contract + property
        results = db.session.execute(
            db.select(tenantModel, propertyModel.house_name)
            .join(contractModel, contractModel.tenant_id == tenantModel.id, isouter=True)
            .join(propertyModel, propertyModel.id == contractModel.property_id, isouter=True)
            .where(tenantModel.user_id == user_data["id"])
        ).all()

        tenants_list = []

        for tenant, house_name in results:
            tenant_dict = {
                "id": tenant.id,
                "name": tenant.name,
                "property_name": house_name 
            }
            tenants_list.append(tenant_dict)

        return jsonify({"tenants": tenants_list})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

