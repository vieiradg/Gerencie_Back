from flask import jsonify

# from flasgger.utils import swag_from
from . import bp_dashboard
from src.model.property_model import propertyModel
from src.model.contract_model import contractModel
from src.model.tenant_model import tenantModel
from src.model import db
from src.security.jwt_config import token_required


@bp_dashboard.route("/documents_panel", methods=["GET"])
@token_required
def documents_panel(user_data):
    try:
        results = db.session.execute(
            db.select(contractModel, tenantModel, propertyModel)
            .join(tenantModel, tenantModel.id == contractModel.tenant_id, isouter=True)
            .join(
                propertyModel,
                propertyModel.id == contractModel.property_id,
                isouter=True,
            )
            .where(contractModel.user_id == user_data["id"])
        ).all()

        contracts_list = []
        for contract, tenant, property in results:
            contract_info = contract.to_dict()
            contract_info.update(
                {
                    "tenant_name": tenant.name if tenant else None,
                    "property_name": property.house_name if property else None,
                }
            )
            contracts_list.append(contract_info)

        tenants = (
            db.session.execute(
                db.select(tenantModel).where(tenantModel.user_id == user_data["id"])
            )
            .scalars()
            .all()
        )

        properties = (
            db.session.execute(
                db.select(propertyModel).where(propertyModel.user_id == user_data["id"])
            )
            .scalars()
            .all()
        )

        # Pega todos os tenant_ids e property_ids que já estão em contrato
        contratados_tenants_ids = [c.tenant_id for c, _, _ in results]
        contratados_properties_ids = [c.property_id for c, _, _ in results]

        # Filtra inquilinos que ainda não estão em contrato
        tenants_list = [
            {"id": tenant.id, "name": tenant.name}
            for tenant in tenants
            if tenant.id not in contratados_tenants_ids
        ]

        # Filtra imóveis que ainda não estão em contrato
        properties_list = [
            {"id": property.id, "name": property.house_name}
            for property in properties
            if property.id not in contratados_properties_ids
        ]

        return (
            jsonify(
                {
                    "contracts": contracts_list,
                    "tenants": tenants_list,
                    "properties": properties_list,
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
