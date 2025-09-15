from flask import request, jsonify  # Importa módulos do Flask
from sqlalchemy import and_
from flasgger.utils import swag_from
from . import bp_property
from src.model.property_model import propertyModel
from src.model import db
from src.security.jwt_config import token_required

@bp_property.route("/register", methods=["POST"])
@token_required
@swag_from("../../docs/property_register.yml")
def register(user_data):
     data = request.get_json()
     user_id = user_data["id"]

     property_exists = db.session.execute(
          db.select(propertyModel).where(
               and_(
                    propertyModel.postal_code == data["postal_code"],
                    propertyModel.house_complement == data["house_complement"],
                    propertyModel.house_number == data["house_number"]
               )
          )
     ).scalar()
          
     if property_exists:
        return jsonify({"message": "Propriedade já cadastrada"}), 400

     property = propertyModel(
          user_id = user_id,
          house_name = data["house_name"],
          house_number=data["house_number"],
          house_complement=data["house_complement"], 
          postal_code=data["postal_code"]    
     )

     try:
          db.session.add(property)
          db.session.commit()
          return jsonify({ "message": "Imóvel cadastrado com sucesso", "property": property.to_dict() }), 201
     except Exception as e:
          db.session.rollback()
          return jsonify({"message": "Erro ao cadastrar Inquilino", "error": str(e)}), 500
