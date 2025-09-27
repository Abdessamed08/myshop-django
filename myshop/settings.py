import os
from pathlib import Path
# Les imports config et os sont NECESSAIRES pour lire les variables d'environnement de Render
from decouple import config 
from django.urls import reverse_lazy
from django.contrib.messages import constants as messages

# --------------------------
# Chemins de base
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------
# Clé secrète (Utilise la variable d'environnement de Render)
# --------------------------
# CRITIQUE: En production, SECRET_KEY DOIT être lue depuis l'environnement
# Si elle n'est pas trouvée, elle utilise une valeur par défaut.
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key') 

# --------------------------
# Mode debug (Désactivé en production pour des raisons de sécurité)
# --------------------------
# CRITIQUE: Désactive le mode DEBUG si SECRET_KEY est définie (donc si nous sommes sur Render)
# La variable de mode DEBUG n'est pas utilisée ici, car nous voulons qu'elle soit FALSE en prod.
DEBUG = (SECRET_KEY == 'django-insecure-your-secret-key') 

# --------------------------
# Hôtes autorisés (Lit la variable de Render et inclut l'URL de secours)
# --------------------------
RENDER_DOMAIN = 'myshop-django-1.onrender.com'
RENDER_HOSTS = [RENDER_DOMAIN]

# La ligne ci-dessous utilise la liste d'hôtes définie sur Render,
# ET ajoute l'URL de secours (votre domaine Render) si elle manque.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',') + RENDER_HOSTS

# Nous ne gérons pas les fichiers statiques de manière avancée sur Render, donc CSRF_TRUSTED_ORIGINS n'est pas toujours nécessaire
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
    # CORRECTION CRITIQUE: Ajout du 'r' manquant ici :
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
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'store',
        'CLIENT': {
            # CORRECTION CRITIQUE: Changement de 'mongodb://' à 'mongodb+srv://'
            # pour résoudre l'erreur DNS (No address associated with hostname) sur Render
            'host': 'mongodb+srv://mezianimohamedabdelsamed_db_user:samedsamed13@cluster0.7k6tbxv.mongodb.net/store?retryWrites=true&w=majority',
        }
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
STATIC_ROOT = BASE_DIR / 'staticfiles'
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