from flask import Blueprint

bp_dashboard  = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# Importa os módulos que registram rotas
from . import control_panel, properties_panel, properties_panel_id, tenants_panel
