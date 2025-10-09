from flask import Blueprint

bp_property = Blueprint("property", __name__, url_prefix="/property")

from . import properties_register 
from . import property_actions    
