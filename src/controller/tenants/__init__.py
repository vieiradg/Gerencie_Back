from flask import Blueprint

bp_tenant = Blueprint("tenant", __name__, url_prefix="/tenant")

# Importa os módulos que registram rotas
from . import tenant_register
