from flask import request, jsonify
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

    for field in [
        "house_name",
        "house_street",
        "house_number",
        "house_complement",
        "city",
        "house_neighborhood",
        "postal_code",
    ]:
        if not data.get(field):
            return jsonify({"message": "Todos os campos são obrigatórios."}), 400

    property_exists = db.session.execute(
        db.select(propertyModel).where(
            and_(
                propertyModel.postal_code == data["postal_code"],
                propertyModel.house_complement == data["house_complement"],
                propertyModel.house_number == data["house_number"],
            )
        )
    ).scalar()

    if property_exists:
        return jsonify({"message": "Propriedade já cadastrada"}), 400

    property = propertyModel(
        user_id=user_id,
        house_name=data["house_name"],
        house_street=data["house_street"],
        house_number=data["house_number"],
        house_complement=data["house_complement"],
        city=data["city"],
        house_neighborhood=data["house_neighborhood"],
        postal_code=data["postal_code"],
    )

    try:
        db.session.add(property)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Imóvel cadastrado com sucesso.",
                    "property": property.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao cadastrar imóvel", "error": str(e)}), 500


@bp_property.route("/properties", methods=["GET"])
@token_required
def get_properties(user_data):
    user_id = user_data["id"]

    try:
        properties = propertyModel.query.filter_by(user_id=user_id).all()

        properties_list = [p.to_dict() for p in properties]

        return jsonify(properties_list), 200

    except Exception as e:
        return jsonify({"message": "Erro ao buscar imóveis", "error": str(e)}), 500


@bp_property.route("/property/<int:property_id>", methods=["GET"])
@token_required
def get_property_details(user_data, property_id):
    user_id = user_data["id"]

    try:
        property_item = propertyModel.query.filter_by(
            id=property_id, user_id=user_id
        ).first()

        if not property_item:
            return jsonify({"message": "Imóvel não encontrado ou não autorizado"}), 404

        return jsonify(property_item.to_dict()), 200

    except Exception as e:
        return (
            jsonify({"message": "Erro ao buscar detalhes do imóvel", "error": str(e)}),
            500,
        )


@bp_property.route("/update/<int:property_id>", methods=["PUT"])
@token_required
def update_property(user_data, property_id):
    user_id = user_data["id"]
    data = request.get_json()

    try:
        property_to_update = propertyModel.query.filter_by(
            id=property_id, user_id=user_id
        ).first()

        if not property_to_update:
            return jsonify({"message": "Imóvel não encontrado ou não autorizado"}), 404

        property_to_update.house_street = data.get(
            "house_street", property_to_update.house_street
        )
        property_to_update.house_number = data.get(
            "house_number", property_to_update.house_number
        )
        property_to_update.house_complement = data.get(
            "house_complement", property_to_update.house_complement
        )
        property_to_update.city = data.get("city", property_to_update.city)
        property_to_update.house_neighborhood = data.get(
            "house_neighborhood", property_to_update.house_neighborhood
        )
        property_to_update.postal_code = data.get(
            "postal_code", property_to_update.postal_code
        )

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Imóvel atualizado com sucesso",
                    "property": property_to_update.to_dict(),
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar imóvel", "error": str(e)}), 500


@bp_property.route("/delete/<int:property_id>", methods=["DELETE"])
@token_required
def delete_property(user_data, property_id):
    user_id = user_data["id"]

    try:
        property_to_delete = propertyModel.query.filter_by(
            id=property_id, user_id=user_id
        ).first()

        if not property_to_delete:
            return jsonify({"message": "Imóvel não encontrado ou não autorizado"}), 404

        db.session.delete(property_to_delete)
        db.session.commit()

        return jsonify({"message": "Imóvel excluído com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao excluir imóvel", "error": str(e)}), 500
