from flask import request, jsonify  # Importa módulos do Flask
from sqlalchemy import or_
from src.security.jwt_config import verify_token
from . import bp_property

from src.model.property_model import propertyModel
from src.model import db

@bp_property.route("/register", methods=["POST"])
def register():
     data = request.get_json()
     token_header = request.headers.get("Authorization")
     print(token_header)

     payload = verify_token(token_header)
     if isinstance(payload, tuple):
          return payload
     user_id = payload["id"]
     
     # property_exists = db.session.execute(db.select(propertyModel).where(or_(
     #      propertyModel.phone_number == data["phone_number"],
     #      propertyModel.cpf == data["cpf"]))).scalar()
          
     # if property_exists:
     #  if property_exists.phone_number == data["phone_number"]:
     #    return jsonify({"message": "Telefone já cadastrado"}), 400
     #  if property_exists.cpf == data["cpf"]:
     #    return jsonify({"message": "CPF já cadastrado"}), 400
          
     property = propertyModel(
          user_id = user_id,
          house_street=data["house_street"],
          house_number=data["house_number"],
          house_complement=data["house_complement"],
          city=data["city"],
          postal_code=data["postal_code"]
          
     )

     try:
          db.session.add(property)
          db.session.commit()
          return jsonify({ "message": "Imóvel cadastrado com sucesso", "property": property.to_dict() }), 201
     except Exception as e:
          db.session.rollback()
          return jsonify({"message": "Erro ao cadastrar Inquilino", "erro": str(e)}), 500
