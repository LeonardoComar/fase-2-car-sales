FROM python:3.13.5-slim

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Adicionar o diretório da aplicação ao PYTHONPATH  
ENV PYTHONPATH=/app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Copiar e instalar dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY app/ .

# Criar diretórios necessários para upload de imagens
RUN mkdir -p static/uploads/cars static/uploads/motorcycles static/uploads/thumbnails/cars static/uploads/thumbnails/motorcycles

# Expor a porta
EXPOSE 8080

# Comando para iniciar o servidor
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]