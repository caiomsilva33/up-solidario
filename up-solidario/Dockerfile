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
# Copia apenas o ficheiro de requisitos primeiro
COPY backend/requirements.txt .
# Instala as dependências. Esta camada fica em cache.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o Código-fonte
# Copia o resto do código da aplicação
COPY backend/ .

# 6. Coletar Ficheiros Estáticos
# CORREÇÃO: Define as settings 'dev' para o build
# Isto corrige o 'ModuleNotFoundError' durante o 'collectstatic'
ENV DJANGO_SETTINGS_MODULE=core.settings.dev
RUN python manage.py collectstatic --noinput

# 7. Comando de Execução (Produção)
# O Gunicorn será usado para servir a aplicação em produção.
# O Render/Fly irá substituir o DJANGO_SETTINGS_MODULE para 'core.settings.prod'.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "core.wsgi:application"]