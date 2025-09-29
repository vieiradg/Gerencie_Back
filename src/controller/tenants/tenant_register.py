from flask import request, jsonify
from sqlalchemy import or_
from flasgger.utils import swag_from
from src.model.tenant_model import tenantModel
from src.model.property_model import propertyModel
from src.model import db
from src.security.jwt_config import token_required
from . import bp_tenant


def clean_data(data):
    cleaned_data = {**data}
    if 'cpf' in cleaned_data:
        cleaned_data['cpf'] = cleaned_data['cpf'].replace('.', '').replace('-', '')
    if 'phone_number' in cleaned_data:
        cleaned_data['phone_number'] = cleaned_data['phone_number'].replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    return cleaned_data


@bp_tenant.route("/register", methods=["POST"])
@token_required
@swag_from("../../docs/tenant_register.yml")
def register(user_data):
    data = request.get_json()
    user_id = user_data["id"]
    cleaned_data = clean_data(data)

    for field in ["name", "cpf", "phone_number"]:
        if not cleaned_data.get(field):
            return jsonify({"message": "Todos os campos são obrigatórios."}), 400

    tenant_exists = tenantModel.query.filter(
        or_(
            tenantModel.phone_number == cleaned_data["phone_number"], 
            tenantModel.cpf == cleaned_data["cpf"],
        )
    ).first()

    if tenant_exists:
        if tenant_exists.phone_number == cleaned_data["phone_number"]:
            return jsonify({"message": "Numero de telefone já cadastrado."}), 400
        if tenant_exists.cpf == cleaned_data["cpf"]:
            return jsonify({"message": "Inquilino já cadastrado."}), 400 
    
    property_id = data.get("property_id")
    if property_id:
        property_occupied = tenantModel.query.filter_by(property_id=property_id).first()
        if property_occupied:
            property_details = propertyModel.query.filter_by(id=property_id).first()
            prop_name = property_details.house_name if property_details and property_details.house_name else "o imóvel selecionado"
            return jsonify({
                "message": f"O imóvel '{prop_name}' já está ocupado por outro inquilino."
            }), 400

    tenant = tenantModel(
        name=cleaned_data["name"],
        user_id=user_id,
        phone_number=cleaned_data["phone_number"],
        cpf=cleaned_data["cpf"],
        property_id=property_id if property_id else None,
    ) 

    try:
        db.session.add(tenant)
        db.session.commit()
        return (
            jsonify( { "message": "Inquilino cadastrado com sucesso.", "tenant": tenant.to_dict(), } ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao cadastrar Inquilino", "error": str(e)}), 500


@bp_tenant.route("/tenants_panel", methods=["GET"])
@token_required
def tenants_panel(user_data):
    user_id = user_data["id"]

    try:
        tenants_query = db.session.query(tenantModel, propertyModel.house_name, propertyModel.house_street, propertyModel.house_number).outerjoin(
            propertyModel, tenantModel.property_id == propertyModel.id
        ).filter(tenantModel.user_id == user_id).all()

        tenants_list = []
        for tenant, house_name, house_street, house_number in tenants_query:
            tenant_dict = tenant.to_dict()
            
            # CORREÇÃO AQUI: Se house_name existir, usamos ele. Se não, montamos com rua e número.
            if house_name:
                 tenant_dict["property_name"] = house_name
            elif house_street and house_number:
                 tenant_dict["property_name"] = f"{house_street}, {house_number}"
            else:
                 tenant_dict["property_name"] = "N/A"
                 
            tenant_dict["status"] = "Em dia"
            tenants_list.append(tenant_dict)

        return jsonify({"tenants": tenants_list}), 200

    except Exception as e:
        print(f"ERRO CRÍTICO NO PAINEL DE INQUILINOS: {e}") 
        return jsonify({"error": "Erro interno ao carregar inquilinos", "details": str(e)}), 500


@bp_tenant.route("/update/<int:tenant_id>", methods=["PUT"])
@token_required
def update_tenant(user_data, tenant_id):
    data = request.get_json()
    user_id = user_data["id"]
    cleaned_data = clean_data(data)

    tenant_to_update = tenantModel.query.filter_by(
        id=tenant_id, user_id=user_id
    ).first()

    if not tenant_to_update:
        return jsonify({"message": "Inquilino não encontrado ou não autorizado"}), 404
        
    tenant_exists = tenantModel.query.filter(
        tenantModel.id != tenant_id, 
        tenantModel.user_id == user_id, 
        or_(
            tenantModel.phone_number == cleaned_data.get("phone_number"), 
            tenantModel.cpf == cleaned_data.get("cpf"),
        )
    ).first()

    if tenant_exists:
        if tenant_exists.phone_number == cleaned_data.get("phone_number"):
            return jsonify({"message": "Número de telefone já cadastrado por outro inquilino."}), 400
        if tenant_exists.cpf == cleaned_data.get("cpf"):
            return jsonify({"message": "CPF já cadastrado por outro inquilino."}), 400


    try:
        property_id = data.get("property_id")
        
        tenant_to_update.name = cleaned_data.get("name", tenant_to_update.name)
        tenant_to_update.phone_number = cleaned_data.get("phone_number", tenant_to_update.phone_number)
        tenant_to_update.cpf = cleaned_data.get("cpf", tenant_to_update.cpf)
        
        if property_id == "":
            tenant_to_update.property_id = None
        else:
            tenant_to_update.property_id = property_id if property_id else tenant_to_update.property_id
        
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Inquilino atualizado com sucesso",
                    "tenant": tenant_to_update.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar inquilino", "error": str(e)}), 500

@bp_tenant.route("/delete/<int:tenant_id>", methods=["DELETE"])
@token_required
def delete_tenant(user_data, tenant_id):
    user_id = user_data["id"]

    try:
        tenant_to_delete = tenantModel.query.filter_by(
            id=tenant_id, user_id=user_id
        ).first()

        if not tenant_to_delete:
            return jsonify({"message": "Inquilino não encontrado ou não autorizado"}), 404

        db.session.delete(tenant_to_delete)
        db.session.commit()

        return jsonify({"message": "Inquilino excluído com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao excluir inquilino", "error": str(e)}), 500