import os
from pathlib import Path
from decimal import Decimal
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────
# SECURITY
# ─────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me')
DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
    ".railway.app",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False

# ─────────────────────────────
# APPLICATIONS
# ─────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'accounts',
]

# ─────────────────────────────
# MIDDLEWARE
# ─────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ─────────────────────────────
# URLS / WSGI
# ─────────────────────────────
ROOT_URLCONF = 'milkproject.urls'
WSGI_APPLICATION = 'milkproject.wsgi.application'

# ─────────────────────────────
# TEMPLATES
# ─────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ─────────────────────────────
# DATABASE (POSTGRES FIRST)
# ─────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL',
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=True,
    )
}

# ─────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────
# STATIC & MEDIA
# ─────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─────────────────────────────
# AUTH REDIRECTS
# ─────────────────────────────
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'accounts:home'
LOGOUT_REDIRECT_URL = 'login'

# ─────────────────────────────
# CSRF
# ─────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://*.railway.app',
]

# ─────────────────────────────
# BUSINESS CONFIG
# ─────────────────────────────
PRICE_PER_LITRE = Decimal(
    os.environ.get("PRICE_PER_LITRE", "50")
)

# ─────────────────────────────
# DEFAULT FIELD
# ─────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────
# SUPERUSER AUTO-CREATION (optional)
# ─────────────────────────────
# If you want to auto-create a superuser at startup, you can add logic in apps.py
# Example snippet (to be placed in accounts/apps.py):
#
# from django.apps import AppConfig
# from django.contrib.auth import get_user_model
# import os
#
# class AccountsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'accounts'
#
#     def ready(self):
#         User = get_user_model()
#         if not User.objects.filter(is_superuser=True).exists():
#             User.objects.create_superuser(
#                 username=os.getenv("DJANGO_SUPERUSER_USERNAME", "admin"),
#                 email=os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com"),
#                 password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "password123")
#             )
