from flask import Blueprint

bp_payment = Blueprint("payment", __name__, url_prefix="/payment")

# Importa os módulos que registram rotas
from . import payment_register
