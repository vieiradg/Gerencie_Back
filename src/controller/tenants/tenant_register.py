from flask import request, jsonify  # Importa módulos do Flask
from sqlalchemy import or_
from src.security.jwt_config import verify_token
from . import bp_tenant

from src.model.tenant_model import tenantModel
from src.model import db

@bp_tenant.route("/register", methods=["POST"])
def register():
     data = request.get_json()
     token_header = request.headers.get("Authorization")
     print(token_header)

     payload = verify_token(token_header)
     if isinstance(payload, tuple):
          return payload
     user_id = payload["id"]
     
     tenant_exists = db.session.execute(db.select(tenantModel).where(or_(
          tenantModel.phone_number == data["phone_number"],
          tenantModel.cpf == data["cpf"]))).scalar()
          
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
          return jsonify({"message": "Erro ao cadastrar Inquilino", "erro": str(e)}), 500
