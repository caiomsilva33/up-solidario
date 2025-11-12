# backend/core/settings/settings.py (FICHEIRO BASE)
#
# Contém todas as configurações comuns que são partilhadas
# entre os ambientes de desenvolvimento (dev) e produção (prod).

from pathlib import Path
import os
import stripe
import dj_database_url

# BASE_DIR aponta para a pasta 'backend/'
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configs de ambiente (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
# são definidas em dev.py e prod.py
ALLOWED_HOSTS = []

# --- APLICAÇÕES ---
INSTALLED_APPS = [
    # Core Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Dev
    'django.contrib.staticfiles',
    
    # Terceiros
    'corsheaders',
    'rest_framework',
    'drf_spectacular',
    
    # Nossas Apps
    'accounts',
    'ongs',
    'campaigns',
    'gamification',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Deve vir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], 'APP_DIRS': True,
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

# --- BASE DE DADOS (Lógica Unificada Dev/Prod) ---
if 'DATABASE_URL' in os.environ:
    # Ambiente de Produção (Render/Fly)
    DATABASES = { 'default': dj_database_url.config(conn_max_age=600, ssl_require=True) }
else:
    # Ambiente de Desenvolvimento Local (Docker-compose)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'db', # Nome do serviço no docker-compose.yml
            'PORT': '5432',
        }
    }

# --- Validação de Senhas ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalização ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Manaus'
USE_I18N = True
USE_TZ = True

# --- Ficheiros Estáticos (Admin CSS/JS) ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Configurações do Projeto ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User' # Nosso modelo de utilizador customizado

# --- Configurações da API (DRF) ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_THROTTLE_CLASSES': ('rest_framework.throttling.AnonRateThrottle', 'rest_framework.throttling.UserRateThrottle'),
    'DEFAULT_THROTTLE_RATES': { 'anon': '10/min', 'user': '100/min' }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Up Solidário API',
    'DESCRIPTION': 'API para a plataforma de doações gamificada Up Solidário.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# --- Configurações de Terceiros ---
# Serão definidos em dev.py e prod.py
CORS_ALLOWED_ORIGINS = [] 
CSRF_TRUSTED_ORIGINS = [] 

# Stripe (lê as chaves do .env)
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
stripe.api_key = STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')