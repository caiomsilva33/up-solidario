# backend/core/settings/prod.py
#
# Configurações para o ambiente de PRODUÇÃO (Render, Fly.io).

from .settings import *

# --- Configurações Específicas de Produção ---

DEBUG = False

# A SECRET_KEY é lida obrigatoriamente das variáveis de ambiente
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Os hosts permitidos são lidos das variáveis de ambiente
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(' ')

# --- Configurações de CORS e CSRF ---

# Apenas os domínios de frontend reais podem aceder à API
CORS_ALLOWED_ORIGINS = [
    'https://www.upsolidario.com.br', # O seu domínio
    # Adicione o seu URL do Render aqui, ex: 'https://up-solidario-web.onrender.com'
]

# Confia nos domínios de frontend para pedidos POST
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# --- Configurações de Segurança (HTTPS) ---

# Força os cookies a serem enviados apenas via HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Confia no cabeçalho do proxy (Render/Fly) para identificar tráfego HTTPS
# CORREÇÃO: Estava 'httpss', o correto é 'https'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Redireciona todo o tráfego HTTP para HTTPS
SECURE_SSL_REDIRECT = True

# Configurações HSTS (Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000 # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Impede o "sniffing" de tipo de conteúdo
SECURE_CONTENT_TYPE_NOSNIFF = True