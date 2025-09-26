# Fichier myshop/settings.py - Version complète et finale

import os
from pathlib import Path
from decouple import config
from django.urls import reverse_lazy
from django.contrib.messages import constants as messages

# --------------------------
# Chemins de base
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------
# Clé secrète (ne la changez pas)
# --------------------------
SECRET_KEY = 'django-insecure-your-secret-key' # Laissez cette ligne telle quelle

# --------------------------
# Mode debug
# --------------------------
DEBUG = True

# --------------------------
# Hôtes autorisés
# --------------------------
ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".ngrok-free.app"]
CSRF_TRUSTED_ORIGINS = ["https://*.ngrok-free.app"]

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
# Base de données (Djongo/MongoDB) - Connexion Atlas RESTAURÉE
# --------------------------
# NOTE: Cette connexion doit maintenant utiliser l'IP statique enregistrée dans le fichier hosts.
# --------------------------
# Base de données (SQLite LOCAL) - Pour contourner le blocage du port mobile
# --------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# --------------------------
# Validation des mots de passe
# --------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
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
# Fichiers statiques (CSS, JS) et médias
# --------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --------------------------
# Redirections d'authentification
# --------------------------
LOGIN_URL = reverse_lazy('accounts:login')
LOGIN_REDIRECT_URL = reverse_lazy('products_app:home')
LOGOUT_REDIRECT_URL = reverse_lazy('products_app:home')

# --------------------------
# Messages Django (compatibles Bootstrap)
# --------------------------
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# --------------------------
# Modèle d'utilisateur personnalisé
# --------------------------
AUTH_USER_MODEL = 'accounts.User'
