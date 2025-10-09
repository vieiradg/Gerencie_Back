import os
from google import genai
from google.genai import types

# Certifique-se de que a variável de ambiente GEMINI_API_KEY está configurada
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não está configurada.")

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_adjustment_suggestion(current_rent, last_adjustment_date, contract_details=""):
    """Gera uma sugestão de reajuste de aluguel usando o Gemini."""
    
    # 1. Definindo o Prompter do Sistema
    # Damos instruções específicas ao modelo para que ele atue como um especialista em mercado.
    system_prompt = (
        "Você é um consultor imobiliário especializado em reajustes de aluguel no Brasil. "
        "Sua função é sugerir um novo valor de aluguel e redigir o texto de notificação para o inquilino. "
        "Use índices de mercado conhecidos como IGP-M, IPCA ou CDI como base de reajuste. "
        "A resposta deve ser formatada estritamente como JSON, com as seguintes chaves: "
        "'suggested_rent_value' (valor numérico sem formatação), 'base_index' (índice usado), "
        "'justification' (justificativa de 2-3 frases) e 'notification_text' (texto completo da notificação)."
    )
    
    # 2. Montando o Conteúdo da Mensagem do Usuário
    user_prompt = f"""
    Preciso de uma sugestão de reajuste e a notificação correspondente para um contrato de aluguel.
    
    Detalhes do Contrato:
    - Valor Atual do Aluguel: R$ {current_rent}
    - Data do Último Reajuste (ou Início do Contrato): {last_adjustment_date}
    - Detalhes Adicionais (opcional): {contract_details}
    
    Qual o valor de aluguel sugerido para hoje, qual o índice utilizado e qual o texto de notificação?
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # Modelo rápido e eficiente para tarefas de texto
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",  # Força o modelo a retornar JSON
                response_schema={
                    "type": "object",
                    "properties": {
                        "suggested_rent_value": {"type": "number"},
                        "base_index": {"type": "string"},
                        "justification": {"type": "string"},
                        "notification_text": {"type": "string"},
                    },
                    "required": ["suggested_rent_value", "base_index", "justification", "notification_text"],
                },
            ),
        )
        # O modelo é forçado a retornar um objeto JSON válido, que está em response.text
        return response.text
    
    except Exception as e:
        print(f"Erro na chamada do Gemini: {e}")
        return None