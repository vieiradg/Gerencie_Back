from flask import Flask  # Framework web principal
from flask_cors import CORS  # Permite requisições de outros domínios (CORS)
from dotenv import load_dotenv
import os

# Importa o blueprint de rotas
from src.controller.user.user_routes import bp_user
from src.rota_teste import bp_teste #apenas para desenvolvimento

# Importa a configuração da aplicação
from config import Config

# from src.model import db  # Descomente quando o model estiver pronto (banco de dados)
from src.model import db

load_dotenv()  

def create_app():
    app = Flask(__name__)
    # Carrega as configurações do objeto Config
    app.config.from_object(Config)

    # Inicializa o banco de dados (descomente quando o model estiver pronto)
    db.init_app(app)

    # Habilita CORS para permitir requisições de qualquer origem
    CORS(app, origins="*")

    # Registra os blueprints
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_teste)

    # Cria as tabelas do banco de dados (descomente quando o model estiver pronto)
    with app.app_context():
        db.create_all()

    return app
