from src.app import create_app  # Importa a função que cria a aplicação Flask
from dotenv import load_dotenv  # Permite carregar variáveis de ambiente do arquivo .env

# Carrega variáveis de ambiente do arquivo .env (útil para desenvolvimento local)
load_dotenv()

# Cria a aplicação Flask
app = create_app()

if __name__ == '__main__':
    # Inicia o servidor Flask em modo debug e acessível externamente (necessário para Docker)
    app.run(debug=True, host='0.0.0.0')
