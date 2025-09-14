from flask import request, jsonify
from flasgger.utils import swag_from
from . import bp_user

from src.model.user_model import userModel
from src.model import db
from src.security.bcrypt_config import check_password
from src.security.jwt_config import create_token

@bp_user.route("/login", methods=["POST"])
@swag_from("../../docs/user_login.yml")
def login():
    data = request.get_json()

    try:
        user = db.session.execute(
            db.select(userModel).where(userModel.email == data["email"])
        ).scalar()

        if not user:
            return jsonify({"message": "Usuário não encontrado"}), 404
        
        if check_password(data["password"], user.password):
            token = create_token({"id": user.id})
            
            user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "cpf": user.cpf
            }
            
            return jsonify({"message": "Login bem-sucedido", "token": token, "user": user_data}), 200
        else:
            return jsonify({"message": "Senha incorreta"}), 401
        
    except Exception as e:
        return jsonify({"message": "Erro ao fazer login", "error": str(e)}), 500