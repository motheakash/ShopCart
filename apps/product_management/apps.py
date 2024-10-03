from django.apps import AppConfig


class ProductManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.product_management'

    def ready(self):
        import apps.product_management.signals  # Import the signals

