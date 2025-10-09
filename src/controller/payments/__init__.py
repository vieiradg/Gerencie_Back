from flask import Blueprint

bp_payment = Blueprint("payment", __name__, url_prefix="/payment") 

from . import payment_register
from . import payment_analysis