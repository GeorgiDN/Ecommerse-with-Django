from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerseApp.payment'

    def ready(self):
        import ecommerseApp.payment.signals
