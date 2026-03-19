import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gradpulse.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = "Grad Admin"
password = "GradP2026"
email = "admin@gradpulse.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created.")
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"Superuser '{username}' updated with new password.")
