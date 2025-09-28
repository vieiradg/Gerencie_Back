import requests
import pytest

BASE_URL = "http://localhost:5000/"

# ----------------- DADOS DE TESTE ----------------- #
# Usuário
name_user = "Usuario Teste"
email = "teste@gmail.com"
senha = "123456"
cpf_user = "00000000000"

# Imóvel
house_name = "Casa Teste"
house_street = "Rua Teste"
house_number = "123"
house_complement = "Complemento Teste"
city = "Cidade Teste"
house_neighborhood = "Bairro Teste"
postal_code = "12345000"

# Inquilino
name_inquilino = "Inquilino Teste"
cpf_inquilino = "11111111111"
phone_number = "11111111111"


# ----------------- URLS ----------------- #
LOGIN_URL = f"{BASE_URL}/user/login"
REGISTER_URL = f"{BASE_URL}/user/register"
DELETE_URL = f"{BASE_URL}/user/delete"
PROPERTY_URL = f"{BASE_URL}/property/register"
PROPERTY_DELETE_URL = f"{BASE_URL}/property/delete"
TENANT_URL = f"{BASE_URL}/tenant/register"
CONTRACT_URL = f"{BASE_URL}/contract/register"


# ----------------- FIXTURE ----------------- #
@pytest.fixture(scope="module")
def auth_token():
    # Garante que o usuário não existe
    requests.delete(DELETE_URL, json={"email": email})

    # Cria usuário
    requests.post(
        REGISTER_URL,
        json={
            "name": name_user,
            "email": email,
            "password": senha,
            "cpf": cpf_user,
        },
    )

    # Faz login e pega token
    login_resp = requests.post(LOGIN_URL, json={"email": email, "password": senha})
    assert login_resp.status_code == 200, f"Erro no login: {login_resp.text}"
    token = login_resp.json().get("token")

    yield token

    # Teardown final → remove usuário e imóvel
    # Se tiver endpoint de deletar imóvel, delete antes do usuário
    requests.delete(DELETE_URL, json={"email": email})



# ----------------- TESTES ----------------- #
class TestRegistro:
    @pytest.mark.parametrize(
        "name_user_input, email_input, password, cpf_user_input, status_code_esperado, mensagem_esperada",
        [
            ("", email, senha, cpf_user, 400, "Todos os campos são obrigatórios."),
            (name_user, "", senha, cpf_user, 400, "Todos os campos são obrigatórios."),
            (name_user, email, "", cpf_user, 400, "Todos os campos são obrigatórios."),
            (name_user, email, senha, "", 400, "Todos os campos são obrigatórios."),
            (name_user, email, senha, cpf_user, 201, "Usuário cadastrado com sucesso"),
            (name_user, email, senha, cpf_user, 400, "Email ou CPF já cadastradoa."),
            (name_user, email, senha, cpf_user, 400, "Email ou CPF já cadastradoa."),
        ],
        ids=[
            "NOME EM BRANCO",
            "EMAIL EM BRANCO",
            "SENHA EM BRANCO",
            "CPF EM BRANCO",
            "CADASTRO SUCESSO",
            "EMAIL DUPLICADO",
            "CPF DUPLICADO",
        ],
    )
    def test_cadastro_usuario(
        self,
        name_user_input,
        email_input,
        password,
        cpf_user_input,
        status_code_esperado,
        mensagem_esperada,
    ):
        dados = {
            "name": name_user_input,
            "email": email_input,
            "password": password,
            "cpf": cpf_user_input,
        }
        response = requests.post(REGISTER_URL, json=dados)
        assert response.status_code == status_code_esperado
        assert mensagem_esperada in response.json().get("message", "")

class TestLogin:
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
        ],
    )
    def test_login_usuario(
        self, email_input, password_input, status_code_esperado, mensagem_esperada
    ):
        dados = {"email": email_input, "password": password_input}
        response = requests.post(LOGIN_URL, json=dados)
        assert response.status_code == status_code_esperado
        assert mensagem_esperada in response.json().get("message", "")

class TestImovel:
    @pytest.mark.parametrize(
        "house_name_input, house_street_input, house_number_input, house_complement_input, city_input, house_neighborhood_input, postal_code_input, status_code_esperado, mensagem_esperada",
        [
            (
                "",
                house_street,
                house_number,
                house_complement,
                city,
                house_neighborhood,
                postal_code,
                400,
                "Todos os campos são obrigatórios.",
            ),
            (
                house_name,
                "",
                house_number,
                house_complement,
                city,
                house_neighborhood,
                postal_code,
                400,
                "Todos os campos são obrigatórios.",
            ),
            (
                house_name,
                house_street,
                "",
                house_complement,
                city,
                house_neighborhood,
                postal_code,
                400,
                "Todos os campos são obrigatórios.",
            ),
            (
                house_name,
                house_street,
                house_number,
                "",
                city,
                house_neighborhood,
                postal_code,
                400,
                "Todos os campos são obrigatórios.",
            ),
            (
                house_name,
                house_street,
                house_number,
                house_complement,
                "",
                house_neighborhood,
                postal_code,
                400,
                "Todos os campos são obrigatórios.",
            ),
            (
                house_name,
                house_street,
                house_number,
                house_complement,
                city,
                "",
                postal_code,
                400,
                "Todos os campos são obrigatórios.",
            ),
            (
                house_name,
                house_street,
                house_number,
                house_complement,
                city,
                house_neighborhood,
                "",
                400,
                "Todos os campos são obrigatórios.",
            ),
            (
                house_name,
                house_street,
                house_number,
                house_complement,
                city,
                house_neighborhood,
                postal_code,
                201,
                "Imóvel cadastrado com sucesso.",
            ),
            (
                house_name,
                house_street,
                house_number,
                house_complement,
                city,
                house_neighborhood,
                postal_code,
                400,
                "Propriedade já cadastrada",
            ),
        ],
        ids=[
            "NOME EM BRANCO",
            "RUA EM BRANCO",
            "NUMERO EM BRANCO",
            "COMPLEMENTO EM BRANCO",
            "CIDADE EM BRANCO",
            "BAIRRO EM BRANCO",
            "CEP EM BRANCO",
            "CADASTRO SUCESSO",
            "IMOVEL JA CADASTRADO",
        ],
    )
    def test_cadastro_imovel(
        self,
        auth_token,
        house_name_input,
        house_street_input,
        house_number_input,
        house_complement_input,
        city_input,
        house_neighborhood_input,
        postal_code_input,
        status_code_esperado,
        mensagem_esperada,
    ):
        headers = {"Authorization": f"Bearer {auth_token}"}
        dados = {
            "house_name": house_name_input,
            "house_street": house_street_input,
            "house_number": house_number_input,
            "house_complement": house_complement_input,
            "city": city_input,
            "house_neighborhood": house_neighborhood_input,
            "postal_code": postal_code_input,
        }
        response = requests.post(PROPERTY_URL, json=dados, headers=headers)
        assert response.status_code == status_code_esperado
        assert mensagem_esperada in response.json().get("message", "")

class TestInquilino:
    @pytest.mark.parametrize(
        "name_input, cpf_input, phone_number_input, status_code_esperado, mensagem_esperada",
        [
            ("", cpf_inquilino, phone_number, 400, "Todos os campos são obrigatórios."),
            ( name_inquilino, "", phone_number, 400, "Todos os campos são obrigatórios.", ),
            ( name_inquilino, cpf_inquilino, "", 400, "Todos os campos são obrigatórios.", ),
            ( name_inquilino, cpf_inquilino, phone_number, 201, "Inquilino cadastrado com sucesso.", ),
            ( name_inquilino, cpf_inquilino, "33016101", 400, "Inquilino já cadastrado."),
            ( "inquilino com o mesmo telefone", "12312312321", phone_number, 400, "Numero de telefone já cadastrado."),
        ],
        ids=[
            "NOME EM BRANCO",
            "CPF EM BRANCO",
            "TELEFONE EM BRANCO",
            "CADASTRO SUCESSO",
            "INQUILINO JA CADASTRADO",
            "TELEFONE JA CADASTRADO",
        ],
    )
    def test_cadastro_inquilino(
        self,
        auth_token,
        name_input,
        cpf_input,
        phone_number_input,
        status_code_esperado,
        mensagem_esperada,
    ):
        headers = {"Authorization": f"Bearer {auth_token}"}
        dados = {
            "name": name_input,
            "cpf": cpf_input,
            "phone_number": phone_number_input,
        }
        response = requests.post(TENANT_URL, json=dados, headers=headers)
        assert response.status_code == status_code_esperado
        assert mensagem_esperada in response.json().get("message", "")        

class TestContrato:
    @pytest.fixture(scope="class")
    def tenant_and_property(self, auth_token):
        """
        Cria um imóvel e um inquilino para serem usados nos testes de contrato.
        Retorna (tenant_id, property_id)
        """
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Cria imóvel
        property_resp = requests.post(
            PROPERTY_URL,
            json={
                "house_name": "Casa do Contrato",
                "house_street": "Rua A",
                "house_number": "10",
                "house_complement": "Bloco 1",
                "city": "Cidade X",
                "house_neighborhood": "Bairro Y",
                "postal_code": "99999999",
            },
            headers=headers,
        )
        property_id = property_resp.json().get("property", {}).get("id")

        # Cria inquilino
        tenant_resp = requests.post(
            TENANT_URL,
            json={
                "name": "Inquilino Contrato",
                "cpf": "22222222222",
                "phone_number": "22222222222",
            },
            headers=headers,
        )
        tenant_id = tenant_resp.json().get("tenant", {}).get("id")

        return tenant_id, property_id

    @pytest.mark.parametrize(
        "tenant_id_input, property_id_input, lease_period, rent_value, due_day, start_date, status_code_esperado, mensagem_esperada",
        [
            ("VALID", "VALID", 12, 1200, 10, "2025-01-01", 201, "Contrato cadastrado com sucesso"),
        ],
        ids=[
            "CADASTRO SUCESSO",
        ],
    )
    def test_cadastro_contrato(
        self,
        auth_token,
        tenant_and_property,
        tenant_id_input,
        property_id_input,
        lease_period,
        rent_value,
        due_day,
        start_date,
        status_code_esperado,
        mensagem_esperada,
    ):
        headers = {"Authorization": f"Bearer {auth_token}"}
        tenant_id, property_id = tenant_and_property

        # Substitui IDs válidos pelos criados no fixture
        if tenant_id_input == "VALID":
            tenant_id_input = tenant_id
        if property_id_input == "VALID":
            property_id_input = property_id

        dados = {
            "tenant_id": tenant_id_input,
            "property_id": property_id_input,
            "lease_period": lease_period,
            "rent_value": rent_value,
            "due_day": due_day,
            "start_date": start_date,
        }

        response = requests.post(CONTRACT_URL, json=dados, headers=headers)
        assert response.status_code == status_code_esperado
        assert mensagem_esperada in response.json().get("message", "")