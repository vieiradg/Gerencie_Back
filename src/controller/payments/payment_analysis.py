from flask import request, jsonify
import json
from google.genai import types # Resolvendo o erro 'types is not defined'
from src.services.gemini_service import client 
from src.security.jwt_config import token_required
# Importe as Models necessárias
from src.model.payment_model import paymentModel # Sua Model
from src.model.contract_model import contractModel # Model para ligar a propriedade
from src.model.property_model import propertyModel # Model para segurança
from . import bp_payment # A Blueprint que criamos

# Função auxiliar para formatar os dados de pagamento (mantida)
def format_payments_for_gemini(payments):
    return "; ".join([
        # Usamos 'new_amount' como valor de referência, 'payment_date' para pontualidade
        f"{p.payment_date.strftime('%b/%Y')}: R${p.new_amount or p.amount_paid} (Status: {p.status})"
        for p in payments
    ])


@bp_payment.route("/<int:property_id>/payment_analysis", methods=["GET"])
@token_required
def get_payment_analysis(user_data, property_id):
    user_id = user_data["id"]
    
    try:
        # 1. SEGURANÇA: Garante que o usuário é o dono da propriedade
        property_item = propertyModel.query.filter_by(id=property_id, user_id=user_id).first()
        if not property_item:
            return jsonify({"message": "Imóvel não encontrado ou não autorizado."}), 404

        # 2. BUSCA O CONTRATO ATIVO (LIGANDO IMÓVEL -> CONTRATO)
        contract = contractModel.query.filter_by(property_id=property_id).first()
        if not contract:
            return jsonify({"message": "Nenhum contrato ativo encontrado para esta propriedade."}), 200

        contract_id = contract.id
        
        # 3. BUSCA OS PAGAMENTOS (LIGANDO CONTRATO -> PAGAMENTOS)
        # Filtramos por status diferente de 'pending' para analisar apenas o que já foi processado
        payments = paymentModel.query.filter(
            paymentModel.contract_id == contract_id,
            paymentModel.status != 'pending' 
        ).order_by(paymentModel.payment_date.desc()).all()

        if not payments:
            return jsonify({"message": "Nenhum pagamento processado encontrado para análise."}), 200
            
    except Exception as e:
        return jsonify({"message": "Erro ao buscar histórico de pagamentos.", "error": str(e)}), 500
    
    # 4. LÓGICA DO GEMINI
    payment_data_string = format_payments_for_gemini(payments)

    system_prompt = (
        "Você é um analista financeiro imobiliário. Sua tarefa é analisar o histórico de pagamentos "
        "e gerar um resumo de pontualidade e um conselho para o proprietário. "
        "A resposta deve ser estritamente formatada em JSON com as chaves: "
        "'summary_score' (string, ex: 'Excelente', 'Razoável', 'Preocupante'), "
        "'analysis_text' (resumo de 2-3 frases sobre a pontualidade e tendências de atraso), "
        "'suggestion' (sugestão de ação para o proprietário)."
    )
    
    user_prompt = f"Analise o seguinte histórico de pagamentos: {payment_data_string}. Gere o resumo no formato JSON."

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "summary_score": {"type": "string"},
                        "analysis_text": {"type": "string"},
                        "suggestion": {"type": "string"},
                    },
                    "required": ["summary_score", "analysis_text", "suggestion"],
                },
            ),
        )

        analysis_data = json.loads(response.text)
        
        return jsonify({
            "message": "Análise de pagamentos gerada com sucesso",
            "analysis": analysis_data,
            # Retorna os pagamentos para a tabela do Front-end
            "payments": [p.to_dict() for p in payments] 
        }), 200

    except Exception as e:
        return jsonify({"message": "Erro ao gerar análise da IA.", "error": str(e)}), 503