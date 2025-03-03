from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerseApp.accounts'

    def ready(self):
        import ecommerseApp.accounts.signals
