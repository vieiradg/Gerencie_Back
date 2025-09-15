from flask import Blueprint

bp_property = Blueprint("property", __name__, url_prefix="/property")

# Importa os módulos que registram rotas
from . import properties_register
