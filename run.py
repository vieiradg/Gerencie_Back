from dotenv import load_dotenv
load_dotenv()

from src.app import create_app  # Importa a função que cria a aplicação Flask


app = create_app()

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
