from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=os.getenv("DJANGO_SUPERUSER_USERNAME", "admin"),
                email=os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com"),
                password=os.getenv("DJANGO_SUPERUSER_PASSWORD", "password123")
            )
