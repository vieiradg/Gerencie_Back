from flask import request, jsonify
from sqlalchemy import or_
from flasgger.utils import swag_from
from src.security.bcrypt_config import hash_password
from src.model.user_model import userModel
from src.model import db
from . import bp_user


@bp_user.route("/register", methods=["POST"])
@swag_from("../../docs/user_register.yml")
def register():
    data = request.get_json()

    for field in ["name", "email", "password", "cpf"]:
        if not data.get(field):
            return jsonify({"message": "Todos os campos são obrigatórios."}), 400

    if data["password"] and len(data["password"]) < 6:
        return jsonify({"message": "Senha deve ter no mínimo 6 caracteres."}), 400

    user_exists = userModel.query.filter(
        or_(userModel.email == data["email"], userModel.cpf == data["cpf"])
    ).first()

    if user_exists:
        if user_exists.email == data["email"]:
            return jsonify({"message": "Email já cadastrado"}), 400

        if user_exists.cpf == data["cpf"]:
            return jsonify({"message": "CPF já cadastrado"}), 400

    hashed = hash_password(data["password"])
    user = userModel(
        name=data["name"], email=data["email"], cpf=data["cpf"], password=hashed
    )

    try:
        db.session.add(user)
        db.session.commit()
        return (
            jsonify({"message": "Usuário cadastrado com sucesso", "id": user.id}),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao cadastrar usuário", "error": str(e)}), 500


@bp_user.route("/delete", methods=["DELETE"])
def delete_user():
    # Pega o email via query param ou JSON
    email = request.args.get("email") or request.json.get("email")

    if not email:
        return jsonify({"message": "Email é obrigatório para deletar usuário"}), 400

    # Busca o usuário
    user = userModel.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {email} deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao deletar usuário", "error": str(e)}), 50
