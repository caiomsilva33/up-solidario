# Dockerfile
#
# Receita para construir a imagem de produção da API Django.

# 1. Imagem Base
FROM python:3.11-slim

# 2. Variáveis de Ambiente Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Diretório de Trabalho
WORKDIR /app

# 4. Instalação de Dependências (Otimizado para Cache)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o Código-fonte
COPY backend/ .

# 6. Coletar Ficheiros Estáticos
# Define as settings 'dev' APENAS para este passo de build
ENV DJANGO_SETTINGS_MODULE=core.settings.dev
RUN python manage.py collectstatic --noinput

# 7. Comando de Execução (Produção)
#
# --- A "ARRUMAÇÃO" ESTÁ AQUI ---
#
# Limpa a variável de ambiente do build
ENV DJANGO_SETTINGS_MODULE=""
#
# Executa o Gunicorn e define explicitamente as settings de 'prod'
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--env", "DJANGO_SETTINGS_MODULE=core.settings.prod", "core.wsgi:application"]