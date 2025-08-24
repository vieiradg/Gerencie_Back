from dotenv import load_dotenv
from flask import jsonify
import jwt

load_dotenv()
import os

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def create_token (dados):
    token = jwt.encode(dados, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido!"}), 401