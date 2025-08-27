from flask import Blueprint, request, jsonify  # Importa módulos do Flask
from . import bp_user

from src.model.user_model import userModel
from src.model import db
from src.security.bcrypt_config import check_password
from src.security.jwt_config import create_token

@bp_user.route("/login", methods=["POST"])
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
            return jsonify({"message": "Login bem-sucedido", "token": token}), 200
        else:
            return jsonify({"message": "Senha incorreta"}),401
        
    except Exception as e:
        return jsonify({"message": "Erro ao fazer login", "erro": str(e)}), 500
