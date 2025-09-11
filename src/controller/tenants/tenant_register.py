from flask import request, jsonify
from sqlalchemy import or_
from flasgger.utils import swag_from
from src.model.tenant_model import tenantModel
from src.model import db
from src.security.jwt_config import token_required
from . import bp_tenant

@bp_tenant.route("/register", methods=["POST"])
@token_required
@swag_from("../../docs/tenant_register.yml")
def register(user_data):
     data = request.get_json()
     user_id = user_data["id"]

     tenant_exists = db.session.execute(
          db.select(tenantModel).where(
               or_(
                    tenantModel.phone_number == data["phone_number"],
                    tenantModel.cpf == data["cpf"]
               )
          )
     ).scalar()
          
     if tenant_exists:
      if tenant_exists.phone_number == data["phone_number"]:
        return jsonify({"message": "Telefone já cadastrado"}), 400
      if tenant_exists.cpf == data["cpf"]:
        return jsonify({"message": "CPF já cadastrado"}), 400
          
     tenant = tenantModel(
          name=data["name"],
          user_id = user_id,
          phone_number=data["phone_number"],
          cpf=data["cpf"]
     )

     try:
          db.session.add(tenant)
          db.session.commit()
          return jsonify({ "message": "Inquilino cadastrado com sucesso", "tenant": tenant.to_dict() }), 201
     except Exception as e:
          db.session.rollback()
          return jsonify({"message": "Erro ao cadastrar Inquilino", "error": str(e)}), 500
