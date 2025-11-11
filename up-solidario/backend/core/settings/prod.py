from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ["up-solidario.fly.dev"]

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}

CSRF_TRUSTED_ORIGINS = ["https://up-solidario.fly.dev"]
