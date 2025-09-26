import json
import os
from django.core.management.base import BaseCommand
from products_app.models import Wilaya, Daira, Commune
from django.conf import settings

class Command(BaseCommand):
    help = 'Charge les données des wilayas, dairas et communes depuis algeria_cities.json'

    def handle(self, *args, **options):
        # Chemin absolu vers le fichier JSON
        file_path = os.path.join(settings.BASE_DIR, 'products_app', 'algeria_cities.json')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Fichier non trouvé : {file_path}"))
            return

        # Charger le JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Supprimer les anciennes données
        Commune.objects.all().delete()
        Daira.objects.all().delete()
        Wilaya.objects.all().delete()

        wilaya_cache = {}  # Pour éviter les doublons
        daira_cache = {}   # Clé: wilaya_name + daira_name

        for entry in data:
            wilaya_name = entry.get('wilaya_name').strip()
            daira_name = entry.get('daira_name').strip()
            commune_name = entry.get('commune_name').strip()

            # Créer ou récupérer la Wilaya
            if wilaya_name not in wilaya_cache:
                wilaya = Wilaya.objects.create(name=wilaya_name)
                wilaya_cache[wilaya_name] = wilaya
            else:
                wilaya = wilaya_cache[wilaya_name]

            # Créer ou récupérer la Daira
            daira_key = f"{wilaya_name}_{daira_name}"
            if daira_key not in daira_cache:
                daira = Daira.objects.create(name=daira_name, wilaya=wilaya)
                daira_cache[daira_key] = daira
            else:
                daira = daira_cache[daira_key]

            # Créer la Commune
            Commune.objects.create(name=commune_name, daira=daira)

        self.stdout.write(self.style.SUCCESS('Toutes les données d’Algérie ont été chargées avec succès !'))
