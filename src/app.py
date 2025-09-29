from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from dotenv import load_dotenv
from .config import Config
from src.model import db

from src.controller.user import bp_user
from src.controller.tenants import bp_tenant
from src.controller.property import bp_property
from src.controller.contracts import bp_contract
from src.controller.payments import bp_payment
from src.controller.dashboard import bp_dashboard

Swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json/",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "bearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer"
        }
    }
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    Swagger(app, config=Swagger_config)
    CORS(app, origins="*")

    app.register_blueprint(bp_user)
    app.register_blueprint(bp_tenant)
    app.register_blueprint(bp_property)
    app.register_blueprint(bp_contract)
    app.register_blueprint(bp_payment)
    app.register_blueprint(bp_dashboard)

    with app.app_context():
        db.create_all()

    return app