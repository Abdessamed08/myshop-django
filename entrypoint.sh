#!/usr/bin/env bash
# Script pour exécuter les tâches de préparation (migration/collecte statique)
# avant de lancer le serveur de production (Gunicorn).

set -o errexit  # Arrête le script si une commande échoue

# 1. Effectuer la collecte des fichiers statiques
echo "-> Démarrage de la collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# 2. Exécuter les migrations de la base de données
echo "-> Exécution des migrations de la base de données..."
python manage.py migrate --noinput

# 3. Lancer le serveur Gunicorn
echo "-> Lancement du serveur Gunicorn..."
# La commande Gunicorn doit être la dernière
exec gunicorn myshop.wsgi:application