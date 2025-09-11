from flask import Blueprint, request, jsonify  # Importa módulos do Flask
from sqlalchemy import or_

from src.model.user_model import userModel
from src.model import db
from src.security.bcrypt_config import hash_password, check_password
from src.security.jwt_config import verify_token

bp_user = Blueprint("user", __name__, url_prefix="/user")