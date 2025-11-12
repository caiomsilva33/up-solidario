# backend/core/settings/dev.py
#
# Configurações para o ambiente de desenvolvimento local (Docker).

from .settings import *

# --- Configurações de Desenvolvimento ---

DEBUG = True

# Chave secreta local, não precisa ser a de produção
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key-local')

# Permite acesso via localhost
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# --- CORREÇÃO DO ERRO DE CORS ---
# Permite que o painel de teste (frontend/index.html), que corre em 'file://',
# acesse a API que corre em 'localhost'. O navegador envia "null" como origem.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "null"  # Permite pedidos de 'file://'
]

# Se o erro de CORS persistir (o que é improvável), descomente a linha abaixo:
# CORS_ORIGIN_ALLOW_ALL = True