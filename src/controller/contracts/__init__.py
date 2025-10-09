from flask import Blueprint

bp_contract = Blueprint("contract", __name__, url_prefix="/contract")

from . import contract_register
from . import contract_actions