from flask import request, jsonify
from flasgger.utils import swag_from
from src.security.jwt_config import create_token
from src.security.bcrypt_config import check_password
from src.model.user_model import userModel
from src.model import db
from . import bp_user

@bp_user.route("/login", methods=["POST"])
@swag_from("../../docs/user_login.yml")
def login():
    data = request.get_json()

    for field in ["email", "password"]:
        if not data.get(field):
            return jsonify({"message": "Todos os campos são obrigatórios."}), 400

    try:
        user_exists = userModel.query.filter(userModel.email == data["email"]).first()

        if not user_exists:
            return jsonify({"message": "Usuário ou senha inválidos."}), 401

        if check_password(data["password"], user_exists.password):
            token = create_token({"id": user_exists.id})

            return (
                jsonify(
                    {
                        "message": "Login realizado com sucesso.",
                        "token": token,
                    }
                ),
                200,
            )
        else:
            return jsonify({"message": "Usuário ou senha inválidos."}), 401

    except Exception as e:
        return jsonify({"message": "Erro ao fazer login", "error": str(e)}), 500
