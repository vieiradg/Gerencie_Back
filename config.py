import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.join(basedir, '..')
load_dotenv(os.path.join(project_root, '.env'))

class Config:
    """Classe de configuração que lê as variáveis do ambiente."""
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("URL_DATABASE_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False