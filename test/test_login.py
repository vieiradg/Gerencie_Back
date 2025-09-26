import requests
import pytest

BASE_URL = "http://localhost:5000/"

# Dados do usuário de teste
email = "teste@gmail.com"
senha = "123456"
cpf = "12345678900"
nome = "Usuário Teste"

LOGIN_URL = f"{BASE_URL}/user/login"
REGISTER_URL = f"{BASE_URL}/user/register"
DELETE_URL = f"{BASE_URL}/user/delete"


# Fixture para preparar o usuário antes dos testes e limpar depois
@pytest.fixture(scope="module")
def user_setup_teardown():
    # Garante que o usuário não existe antes de começar
    requests.delete(DELETE_URL, json={"email": email})

    # Cria o usuário para testes de login
    requests.post(REGISTER_URL, json={
        "name": nome,
        "email": email,
        "password": senha,
        "cpf": cpf
    })

    yield

    # Remove o usuário após os testes
    requests.delete(DELETE_URL, json={"email": email})


# Testes de login
@pytest.mark.parametrize(
    "email_input, password_input, status_code_esperado, mensagem_esperada",
    [
        ("", senha, 400, "Todos os campos são obrigatórios."),
        (email, "", 400, "Todos os campos são obrigatórios."),
        ("naoexiste@gmail.com", senha, 401, "Usuário ou senha inválidos."),
        (email, "senhaerrada", 401, "Usuário ou senha inválidos."),
        (email, senha, 200, "Login realizado com sucesso."),
    ],
    ids=[
        "EMAIL EM BRANCO",
        "SENHA EM BRANCO",
        "EMAIL NAO CADASTRADO",
        "SENHA INCORRETA",
        "LOGIN EFETUADO",
    ]
)
def test_login(user_setup_teardown, email_input, password_input, status_code_esperado, mensagem_esperada):
    dados = {"email": email_input, "password": password_input}
    response = requests.post(LOGIN_URL, json=dados)

    assert response.status_code == status_code_esperado, (
        f"Esperado {status_code_esperado}, mas retornou {response.status_code}"
    )

    mensagem_resposta = response.json().get("message", "")
    assert mensagem_esperada in mensagem_resposta, (
        f"Mensagem esperada: '{mensagem_esperada}', mas recebeu: '{mensagem_resposta}'"
    )
