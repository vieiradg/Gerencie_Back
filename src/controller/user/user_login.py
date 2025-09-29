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
        user_exists = userModel.query.filter_by(email=data["email"]).first()

        if not user_exists:
            return jsonify({"message": "Usuário ou senha inválidos."}), 401

        if not check_password(data["password"], user_exists.password):
            return jsonify({"message": "Usuário ou senha inválidos."}), 401

        token_data = {"id": user_exists.id} 
        token = create_token(token_data)

        user_data = {"id": user_exists.id, "email": user_exists.email, "name": user_exists.name}

        return (
            jsonify(
                {
                    "message": "Login realizado com sucesso.",
                    "token": token,
                    "user": user_data, 
                }
            ),
            200,
        )

    except Exception as e:
        print(f"ERRO DE LOGIN CRÍTICO: {e}")
        return jsonify({"message": "Erro interno ao processar login", "error": str(e)}), 500