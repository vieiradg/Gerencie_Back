from flask import request, jsonify  # Importa módulos do Flask
from sqlalchemy import or_
from . import bp_user

from src.model.user_model import userModel
from src.model import db
from src.security.bcrypt_config import hash_password, check_password
from src.security.jwt_config import create_token

@bp_user.route("/register", methods=["POST"])
def register():
     data = request.get_json()
     
     user_exists = db.session.execute(db.select(userModel).where(or_(
          userModel.email == data["email"],
          userModel.cpf == data["cpf"]
     ))).scalar()
          
     if user_exists:
      if user_exists.email == data["email"]:
        return jsonify({"message": "Email já cadastrado"}), 400
      if user_exists.cpf == data["cpf"]:
        return jsonify({"message": "CPF já cadastrado"}), 400
          
     hashed = hash_password(data["password"])
     user = userModel(
          name=data["name"],
          email=data["email"],
          password=hashed,
          cpf=data["cpf"]
     )

     try:
          db.session.add(user)
          db.session.commit()
          return jsonify({"message": "Usuário cadastrado com sucesso", "id": user.id}), 201
     except Exception as e:
          db.session.rollback()
          return jsonify({"message": "Erro ao cadastrar usuário", "erro": str(e)}), 500
