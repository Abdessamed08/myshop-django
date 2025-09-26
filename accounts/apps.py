from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Cette ligne est maintenant à l'intérieur de la classe
        import accounts.models  # Ou accounts.signals si vous l'avez créé