from flask import Blueprint

bp_user = Blueprint("user", __name__, url_prefix="/user")

# Importa os módulos que registram rotas
from . import user_login, user_register, user_delete_testes
