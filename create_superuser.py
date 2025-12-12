from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

username = "kiruba_karan_123"
password = "kiruba@123"
email = "dhayalankiruba17@gmail.com"

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email=email)
        print("Superuser created")
    else:
        print("Superuser already exists")
except IntegrityError:
    print("Error creating superuser")
