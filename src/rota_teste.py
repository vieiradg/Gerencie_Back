from flask import Blueprint, request, jsonify  # Importa módulos do Flask
from src.model.user_model import userModel
from src.model import db
from sqlalchemy import text
bp_teste = Blueprint('teste', __name__)

@bp_teste.route('/teste', methods=['GET'])
def teste():
    db_status = "Não testado ainda"
    
    try:
        # Consulta mínima apenas para testar conexão
        result = db.session.execute(text("SELECT 1")).scalar()
        if result == 1:
            db_status = "Conexao com Postgres OK"
        else:
            db_status = "Conexao estabelecida, mas retorno inesperado"
    except Exception as e:
        db_status = f"Erro ao conectar no banco: {str(e)}"
    
    return jsonify({
        "mensagem": "Parabens, o servidor esta funcionando!",
        "db_status": db_status
    })