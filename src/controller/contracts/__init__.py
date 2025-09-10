from flask import Blueprint

bp_contract = Blueprint("contract", __name__, url_prefix="/contract")

# Importa os módulos que registram rotas
from . import contract_register
