import requests
import pytest

BASE_URL = "http://localhost:5000/"

# Dados do usuário de teste
nome = "User Teste"
email = "teste@gmail.com"
senha = "123456"
cpf = "00000000000"


# Fixture que cria o usuário antes dos testes e deleta depois
@pytest.fixture(scope="module")
def user_setup_teardown():
    # Setup: garante que não existe usuário antes de começar
    requests.delete(f"{BASE_URL}/user/delete", json={"email": email})
    yield
    # Teardown: deleta o usuário após todos os testes do módulo
    requests.delete(f"{BASE_URL}/user/delete", json={"email": email})


@pytest.mark.parametrize(
    "name, email_input, password, cpf_input, status_code_esperado, mensagem_esperada",
    [
        ("", email, senha, cpf, 400, "Todos os campos são obrigatórios."),
        (nome, "", senha, cpf, 400, "Todos os campos são obrigatórios."),
        (nome, email, "", cpf, 400, "Todos os campos são obrigatórios."),
        (nome, email, senha, "", 400, "Todos os campos são obrigatórios."),
        (nome, "email_invalido", senha, cpf, 400, "Email com formato inválido."),
        (nome, email, "123", cpf, 400, "Senha deve ter no mínimo 6 caracteres."),
        (nome, email, senha, cpf, 201, "Usuário cadastrado com sucesso"),
        (nome, email, senha, "email_duplicado", 400, "Email já cadastrado"),
        (nome, "cpf_duplicado", senha, cpf, 400, "CPF já cadastrado"),
    ],
    ids=[
        "NOME EM BRANCO",
        "EMAIL EM BRANCO",
        "SENHA EM BRANCO",
        "CPF EM BRANCO",
        "EMAIL INVALIDO",
        "SENHA CURTA",
        "CADASTRO SUCESSO",
        "EMAIL DUPLICADO",
        "CPF DUPLICADO",
    ],
)
def test_register(
    name, email_input, password, cpf_input, status_code_esperado, mensagem_esperada
):
    dados = {
        "name": name,
        "email": email_input,
        "password": password,
        "cpf": cpf_input,
    }

    response = requests.post(f"{BASE_URL}/user/register", json=dados)
    assert (
        status_code_esperado == response.status_code
    ), f"ESPERANDO {status_code_esperado}, RETORNO {response.status_code}"
    mensagem_resposta = response.json().get("message", "")
    assert (
        mensagem_esperada in mensagem_resposta
    ), f"Mensagem esperada: '{mensagem_esperada}', mas recebeu: '{mensagem_resposta}'"
