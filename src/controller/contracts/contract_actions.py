from flask import request, jsonify
import json
from google.genai import types
from src.services.gemini_service import client
from src.model.contract_model import contractModel
from src.model.property_model import propertyModel
from src.model.tenant_model import tenantModel
from src.model.user_model import userModel  # Necessário para buscar o Locador (Proprietário)
from src.security.jwt_config import token_required
from . import bp_contract

# =================================================================
# 1. ENDPOINT PARA BUSCAR O CONTRATO ATIVO PELO ID DO IMÓVEL
# =================================================================

@bp_contract.route("/property/<int:property_id>", methods=["GET"])
@token_required
def get_contract_by_property(user_data, property_id):
    user_id = user_data["id"]

    try:
        contract = contractModel.query.filter_by(
            property_id=property_id, 
            user_id=user_id,
        ).first()

        if not contract:
            return jsonify({"message": "Nenhum contrato ativo encontrado para este imóvel."}), 404

        tenant = tenantModel.query.get(contract.tenant_id)
        
        contract_data = contract.to_dict()
        contract_data['tenant_name'] = tenant.name if tenant else 'Inquilino Removido'
        
        return jsonify(contract_data), 200

    except Exception as e:
        print(f"ERRO BUSCA DE CONTRATO POR IMÓVEL: {e}")
        return jsonify({"message": "Erro interno ao buscar contrato"}), 500


# =================================================================
# 2. ENDPOINT PARA GERAR O TEXTO LEGAL VIA GEMINI (ATUALIZADO)
# =================================================================

@bp_contract.route("/<int:contract_id>/generate_text", methods=["GET"])
@token_required
def generate_contract_text(user_data, contract_id):
    user_id = user_data["id"]

    try:
        # 1. Busca os dados essenciais (Contrato, Locador, Imóvel, Inquilino)
        contract = contractModel.query.filter_by(id=contract_id, user_id=user_id).first()
        if not contract:
            return jsonify({"message": "Contrato não encontrado ou não autorizado"}), 404

        property_ = propertyModel.query.get(contract.property_id)
        tenant = tenantModel.query.get(contract.tenant_id)
        locador = userModel.query.get(user_id) # Busca os dados do proprietário/usuário logado
        
        if not property_ or not tenant or not locador:
            return jsonify({"message": "Dados de contrato incompletos (Imóvel, Inquilino ou Locador não encontrados)"}), 404
        
        # 2. Monta o Prompt de Contexto para a IA
        
        system_prompt = (
            "Você é um advogado especialista em direito imobiliário brasileiro. "
            "Sua tarefa é gerar o texto completo de um Contrato de Locação Residencial Padrão, em formato Markdown. "
            "O contrato será assinado digitalmente e não exige a figura de testemunhas. Remova qualquer menção a testemunhas no corpo e no final do documento. "
            "Use linguagem formal/jurídica (usando ## para cláusulas e **negrito** para termos importantes)."
        )

        user_prompt = f"""
        Gere um Contrato de Locação Residencial com base nos seguintes termos:
        
        - **Locador (Proprietário):** {locador.name} (CPF: {locador.cpf}).
        - **Imóvel (Objeto):** {property_.house_name}, {property_.house_street}, {property_.house_number}, {property_.house_neighborhood} - {property_.city}, CEP {property_.postal_code}.
        - **Locatário (Inquilino):** {tenant.name}, CPF {tenant.cpf}.
        - **Valor do Aluguel:** R$ {contract.rent_value}.
        - **Prazo (Período):** {contract.lease_period} meses.
        - **Início/Término:** {contract.start_date} a {contract.end_date}.
        - **Dia de Vencimento:** Todo dia {contract.due_day} de cada mês.
        - **Índice de Reajuste:** IGPM/FGV.
        """

        # 3. Chama a API do Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )
        
        return jsonify({
            "message": "Contrato gerado com sucesso",
            "contract_text": response.text
        }), 200

    except Exception as e:
        print(f"ERRO GERAÇÃO DE CONTRATO: {e}")
        return jsonify({"message": "Erro interno ao gerar contrato"}), 500