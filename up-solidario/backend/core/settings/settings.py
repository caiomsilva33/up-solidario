# api/core/settings.py

from pathlib import Path
import os
import stripe
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-11m023y#o7vqn4osi@y83xtpce&ql(!*a6v!&n@y+&*d&*en(8') # Substitua pelo seu secret key original como fallback
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS_STRING = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1')
ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(' ') if ALLOWED_HOSTS_STRING else []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'corsheaders',
    # Nossas apps
    'accounts',
    'ongs',
    'campaigns',
    'gamification',
    # Apps de terceiros
    'rest_framework',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --- CONFIGURAÇÃO DA BASE DE DADOS (Agora para Dev e Prod) ---
# Esta lógica verifica se estamos em produção (se a variável DATABASE_URL existe).
# Se sim, usa-a. Se não, usa a nossa configuração local do Docker.
if 'DATABASE_URL' in os.environ:
    # Ambiente de Produção (Fly.io)
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    # Ambiente de Desenvolvimento Local (Docker)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'up_solidario_db',
            'USER': 'admin',
            'PASSWORD': 'supersecretpassword',
            'HOST': 'db',
            'PORT': '5432',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # --- OTIMIZAÇÃO DE PERFORMANCE: PAGINAÇÃO ---
    # Ativa a paginação para toda a API, retornando 100 itens por página.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,

        # --- Configuração de Rate Limiting ---
    'DEFAULT_THROTTLE_CLASSES': [
        # Limita pedidos anónimos com base no IP.
        'rest_framework.throttling.AnonRateThrottle',
        # Limita pedidos de utilizadores autenticados com base no ID do utilizador.
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        # Define o limite: 10 pedidos por minuto para utilizadores anónimos.
        'anon': '10/min',
        # Define o limite: 100 pedidos por minuto para utilizadores autenticados.
        'user': '100/min'
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Up Solidário API',
    'DESCRIPTION': 'API para a plataforma de doações gamificada Up Solidário. Documentação completa de todos os endpoints disponíveis.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]

# Stripe configuration
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
stripe.api_key = STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

# --- Configuração de Segurança Adicional para Deploy ---

# Diz ao Django para confiar em pedidos POST vindos do nosso domínio de produção.
# Certifique-se de que inclui o 'https://'.
CSRF_TRUSTED_ORIGINS = ['https://up-solidario.fly.dev']

# Opcional, mas altamente recomendado para produção:
# Garante que os cookies de sessão e CSRF só são enviados através de uma ligação segura (HTTPS).
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# --- Configuração de Segurança Adicional para Deploy ---

# Diz ao Django para confiar em pedidos POST vindos dos nossos domínios de produção.
CSRF_TRUSTED_ORIGINS = ['https://www.upsolidario.com.br', 'https://up-solidario.fly.dev']

# Garante que os cookies de sessão e CSRF só são enviados através de uma ligação segura (HTTPS).
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# --- A LINHA NOVA E CRUCIAL ---
# Diz ao Django para confiar no cabeçalho X-Forwarded-Proto que o proxy do Fly.io envia,
# para que ele saiba que a ligação original era HTTPS. Isto é essencial para o CSRF funcionar.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- Configuração de Cabeçalhos de Segurança ---
# Garante que todo o tráfego para o seu site seja redirecionado para HTTPS.
SECURE_SSL_REDIRECT = True
# Impede que o navegador adivinhe o tipo de conteúdo dos ficheiros, prevenindo ataques.
SECURE_CONTENT_TYPE_NOSNIFF = True
# Ativa a proteção HSTS, dizendo ao navegador para apenas comunicar com o seu site via HTTPS.
SECURE_HSTS_SECONDS = 31536000 # (1 ano)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True