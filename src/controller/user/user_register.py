from flask import Blueprint, request, jsonify  # Importa módulos do Flask
from src.model.user_model import userModel
from src.model import db

# Cria um blueprint para rotas relacionadas ao usuário
bp_user = Blueprint("user", __name__, url_prefix="/user")

@bp_user.route("/register", methods=["POST"])
def register():
     data = request.get_json()  # pega os dados enviados no corpo da requisição

     # Validação de campos obrigatorios
     required_fields = ["nome", "email", "senha"]

     # cria o objeto do usuário
     user = userModel(
          name=data["name"],
          email=data["email"],
          password=data["password"],  # mais tarde pode usar hash de senha
          cpf=data["cpf"]
     )

     # adiciona no banco
     db.session.add(user)
     db.session.commit()

     return jsonify({"message": "Usuário cadastrado com sucesso", "id": user.id}), 201