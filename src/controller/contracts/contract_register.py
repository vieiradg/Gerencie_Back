from flask import request, jsonify
from sqlalchemy import and_
from flasgger.utils import swag_from
from . import bp_contract
from src.model.contract_model import contractModel
from src.model.property_model import propertyModel
from src.model import db
from src.security.jwt_config import token_required

@bp_contract.route("/register", methods=["POST"])
@token_required
@swag_from("../../docs/contract_register.yml")
def register(user_data):
     data = request.get_json()
     user_id = user_data["id"]

     property_exists = db.session.get(propertyModel, data["property_id"])

     if not property_exists:
          return jsonify({"message": "Imóvel não encontrado"}), 404

     contract_exists = db.session.execute(
          db.select(contractModel).where(
          and_(
               contractModel.tenant_id == data["tenant_id"],
               contractModel.property_id == data["property_id"],
          ))).scalar_one_or_none()

     if contract_exists:
          return jsonify({"message": "Inquilino já possui contrato nesse imóvel"}), 400

     contract = contractModel(
        user_id=user_id,
        tenant_id=data["tenant_id"],
        property_id=data["property_id"],
        lease_period=data["lease_period"],
        rent_value=data["rent_value"],
        due_day=data["due_day"],
        start_date=data["start_date"]
)

     try:
          db.session.add(contract)
          db.session.commit()
          return jsonify({ "message": "Imóvel cadastrado com sucesso", "contract": contract.to_dict() }), 201
     except Exception as e:
          db.session.rollback()
          return jsonify({"message": "Erro ao cadastrar Inquilino", "error": str(e)}), 500
