import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "milkproject.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "kiruba_karan_123"   # MUST exist already

try:
    user = User.objects.get(username=username)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("User promoted to superuser")
except User.DoesNotExist:
    print("User does NOT exist")
