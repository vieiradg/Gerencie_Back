from os import environ

class Config:
    """
    Classe de configuração da aplicação Flask.
    As variáveis são lidas do ambiente (útil para Docker e segurança).
    """
    # URI de conexão com o banco de dados (PostgreSQL)
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD')
    # Desabilita notificações de modificação do SQLAlchemy (melhora performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Chave secreta para sessões e segurança
    SECRET_KEY = environ.get("SECRET_KEY")
