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

def verify_token(token_header):
    if not token_header or not token_header.startswith("Bearer "):
        return jsonify({"erro": "Token não fornecido"}), 401
    
    token = token_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido!"}), 401