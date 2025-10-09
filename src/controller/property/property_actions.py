from flask import request, jsonify
import json

# CORREÇÃO: Importa a Blueprint do módulo atual (da pasta property)
from . import bp_property 

from src.model.property_model import propertyModel
from src.security.jwt_config import token_required
from src.services.gemini_service import generate_adjustment_suggestion


@bp_property.route("/<int:property_id>/suggest_adjustment", methods=["POST"])
@token_required
def suggest_adjustment(user_data, property_id):
    user_id = user_data["id"]
    data = request.get_json()
    
    current_rent = data.get("current_rent")
    last_adjustment_date = data.get("last_adjustment_date")
    contract_details = data.get("contract_details", "")
    
    if not current_rent or not last_adjustment_date:
        return jsonify({"message": "Valor atual do aluguel e data do último reajuste são obrigatórios."}), 400

    try:
        property_item = propertyModel.query.filter_by(
            id=property_id, user_id=user_id
        ).first()

        if not property_item:
            return jsonify({"message": "Imóvel não encontrado ou não autorizado"}), 404
        
        gemini_response_json = generate_adjustment_suggestion(
            current_rent=current_rent, 
            last_adjustment_date=last_adjustment_date, 
            contract_details=contract_details
        )
        
        if not gemini_response_json:
            return jsonify({"message": "Não foi possível gerar a sugestão de reajuste. Tente novamente."}), 503

        suggestion_data = json.loads(gemini_response_json)
        
        return jsonify({
            "message": "Sugestão de reajuste gerada com sucesso",
            "suggestion": suggestion_data
        }), 200

    except ValueError:
        return jsonify({"message": "Erro ao processar a resposta da IA. Formato inválido."}), 500
    except Exception as e:
        return jsonify({"message": "Erro interno do servidor", "error": str(e)}), 500