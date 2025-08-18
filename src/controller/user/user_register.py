from flask import Blueprint, request, jsonify  # Importa módulos do Flask
from sqlalchemy import or_

from src.model.user_model import userModel
from src.model import db
from src.security.bcrypt_config import hash_password, check_password

# Cria um blueprint para rotas relacionadas ao usuário
bp_user = Blueprint("user", __name__, url_prefix="/user")

@bp_user.route("/register", methods=["POST"])
def register():
     data = request.get_json()  # pega os dados enviados no corpo da requisição

     #verificação de usuario cadastrado
     
     user_exists = db.session.execute(db.select(userModel).where(or_(
          userModel.email == data["email"],
          userModel.cpf == data["cpf"]))).scalar()
          
     if user_exists:
      if user_exists.email == data["email"]:
        return jsonify({"message": "Email já cadastrado"}), 400
      if user_exists.cpf == data["cpf"]:
        return jsonify({"message": "CPF já cadastrado"}), 400
          
          
     # cria o objeto do usuário
     user = userModel(
          name=data["name"],
          email=data["email"],
          password=hash_password(data["password"]),  # mais tarde pode usar hash de senha
          cpf=data["cpf"]
     )

     # adiciona no banco
     try:
          db.session.add(user)
          db.session.commit()
          return jsonify({"message": "Usuário cadastrado com sucesso", "id": user.id}), 201
     except Exception as e:
          db.session.rollback()
          return jsonify({"message": "Erro ao cadastrar usuário", "erro": str(e)}), 500
          
