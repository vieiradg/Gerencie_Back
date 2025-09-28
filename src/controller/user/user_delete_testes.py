from flask import request, jsonify
from sqlalchemy import or_
from flasgger.utils import swag_from
from src.security.bcrypt_config import hash_password
from src.model.user_model import userModel
from src.model import db
from . import bp_user


@bp_user.route("/delete", methods=["DELETE"])
def delete_user():
    data = request.get_json(silent=True) or {}
    email = request.args.get("email") or data.get("email")

    if not email:
        return jsonify({"message": "Email é obrigatório"}), 400

    user = userModel.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {email} deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao deletar usuário", "error": str(e)}), 500
