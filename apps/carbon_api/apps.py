# apps/carbon_api/apps.py
from django.apps import AppConfig


class CarbonApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.carbon_api'
    verbose_name = 'Carbon API'
    
    def ready(self):
        # Import signal handlers if you have any
        pass