import os
from pathlib import Path

# --------------------------
# Chemins de base
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------
# Clé secrète (à remplacer par ta vraie clé)
# --------------------------
SECRET_KEY = 'django-insecure-your-secret-key'

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
# myshop/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products_app',
    'accounts.apps.AccountsConfig', # 🚨 Correction ici 🚨
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
        'DIRS': [BASE_DIR / "templates"],  # ton dossier templates
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
# Base de données (SQLite)
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
# Static files (CSS, JS)
# --------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# --------------------------
# Médias (images, fichiers uploadés)
# --------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --------------------------
# URL par défaut après login (optionnel)
# --------------------------
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# à ajouter à la fin
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEBUG = True

# Redirections utiles
from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('accounts:login')
LOGIN_REDIRECT_URL = reverse_lazy('products_app:home')
LOGOUT_REDIRECT_URL = reverse_lazy('products_app:home')



# Classes de message compatibles Bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

AUTH_USER_MODEL = 'accounts.User'
