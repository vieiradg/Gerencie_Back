from flask import Flask  # Framework web principal
from flask_cors import CORS  # Permite requisições de outros domínios (CORS)
from dotenv import load_dotenv
from src.rota_teste import bp_teste #apenas para desenvolvimento
from config import Config
from src.controller.user import bp_user
from src.model import db

import os

load_dotenv()  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    CORS(app, origins="*")

    app.register_blueprint(bp_user)
    app.register_blueprint(bp_teste)

    with app.app_context():
        db.create_all()

    return app
