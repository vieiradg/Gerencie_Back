FROM python:3.12

# Evita buffering no log
ENV PYTHONUNBUFFERED=1

# Cria diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta
EXPOSE 5000

# Comando para iniciar a app
# O docker-compose.yml irá sobrescrever este comando, mas é bom tê-lo aqui
CMD ["flask", "--app", "run", "run", "--host=0.0.0.0", "--debug"]


