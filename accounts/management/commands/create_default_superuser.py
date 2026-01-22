from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create default superuser if not exists"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "kiruba_karan_123")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "dhayalankiruba17@gmail.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "kiruba@123")

        if User.objects.filter(username=username).exists():
            self.stdout.write("ℹ️ Superuser already exists")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write("✅ Superuser created successfully")
