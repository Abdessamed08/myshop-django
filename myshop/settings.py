import os
from pathlib import Path
from decouple import config  # Pour lire les variables d'environnement
from django.urls import reverse_lazy
from django.contrib.messages import constants as messages

# --------------------------
# Chemins de base
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------
# Clé secrète (tirée de l'environnement Render)
# --------------------------
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key')

# --------------------------
# Mode debug
# --------------------------
DEBUG = (SECRET_KEY == 'django-insecure-your-secret-key')

# --------------------------
# Hôtes autorisés
# --------------------------
RENDER_DOMAIN = 'myshop-django-1.onrender.com'
RENDER_HOSTS = [RENDER_DOMAIN]

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',') + RENDER_HOSTS

CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]

# --------------------------
# Applications installées
# --------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products_app',
    'accounts.apps.AccountsConfig',
    'widget_tweaks',
    'django_extensions',
]

# --------------------------
# Middleware
# --------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------
# URL racine
# --------------------------
ROOT_URLCONF = 'myshop.urls'

# --------------------------
# Templates
# --------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

# --------------------------
# WSGI
# --------------------------
WSGI_APPLICATION = 'myshop.wsgi.application'

# --------------------------
# Base de données (MongoDB via Djongo)
# --------------------------
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'store',
        'CLIENT': {
            'host': config('MONGO_URI'),  # >>> lus depuis l'environnement
        }
    }
}

# --------------------------
# Validation des mots de passe
# --------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------
# Internationalisation
# --------------------------
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --------------------------
# Fichiers statiques & médias
# --------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --------------------------
# Redirections login/logout
# --------------------------
LOGIN_URL = reverse_lazy('accounts:login')
LOGIN_REDIRECT_URL = reverse_lazy('products_app:home')
LOGOUT_REDIRECT_URL = reverse_lazy('products_app:home')

# --------------------------
# Messages Django (Bootstrap)
# --------------------------
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# --------------------------
# Modèle d’utilisateur custom
# --------------------------
AUTH_USER_MODEL = 'accounts.User'
