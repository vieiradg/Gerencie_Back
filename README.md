# Gerencie - Projeto Flask com Docker

Este projeto é um projeto de aplicação Flask estruturada para uso com Docker e PostgreSQL, com suporte a variáveis de ambiente e organização modular.

## Estrutura do Projeto

```
config.py                # Configurações globais da aplicação
requirements.txt         # Dependências Python
Dockerfile               # Imagem Docker da aplicação
run.py                   # Ponto de entrada da aplicação
src/
  app.py                 # Criação e configuração da aplicação Flask
  controller/
    user/
      user_register.py   # Blueprint de rotas de usuário
```

## Principais Arquivos

- **config.py**: Define as configurações da aplicação, como URI do banco e chave secreta, usando variáveis de ambiente.
- **run.py**: Ponto de entrada. Carrega variáveis do `.env` (em desenvolvimento) e inicia o servidor Flask.
- **src/app.py**: Função `create_app()` que monta a aplicação, registra blueprints e configura CORS.
- **src/controller/user/user_register.py**: Define rotas relacionadas ao usuário usando Blueprint.
- **requirements.txt**: Lista de dependências Python.
- **Dockerfile**: Define como construir a imagem Docker da aplicação.
- **docker-compose.yml**: Orquestra a aplicação e o banco de dados PostgreSQL em containers.


## Como rodar com Docker

1. No arquivo `env.example` altere para `.env` e coloque suas variaves de ambiente:

2. Construa e suba os containers:
   ```bash
   docker-compose up --build
   ```
3. Acesse a aplicação em `http://localhost:5000/teste`:
    ```
    {
    "mensagem": "Parabans, o servidor esta funcionando!"
    "db_status": "Conexao com Postgres OK",
    }
    ```
