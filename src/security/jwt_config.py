from functools import wraps
from dotenv import load_dotenv
from flask import jsonify, request
from datetime import datetime, timedelta
import jwt
import os
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 12))

def create_token(dados):
    expiracao = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {**dados, "exp": expiracao}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_header = request.headers.get("Authorization")

        if not token_header or not token_header.startswith("Bearer "):
            return jsonify({"error": "Token não fornecido"}), 401

        token = token_header.split(" ")[1]

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido!"}), 401

        return f(payload, *args, **kwargs)

    return decorated