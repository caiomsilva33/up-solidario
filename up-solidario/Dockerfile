# Dockerfile (na raiz do projeto)

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Aponta para o requirements.txt dentro da pasta 'backend'
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da pasta 'backend' para o diretório de trabalho
COPY backend/ .

# Comandos de Produção
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "core.wsgi:application"]