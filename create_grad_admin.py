import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gradpulse.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def ensure_admin(uname, email, pwd):
    if not User.objects.filter(username=uname).exists():
        user = User.objects.create_superuser(uname, email, pwd)
        user.portal_type = 'employer'
        user.save()
        print(f"Superuser '{uname}' created.")
    else:
        user = User.objects.get(username=uname)
        user.set_password(pwd)
        user.is_superuser = True
        user.is_staff = True
        user.portal_type = 'employer'
        user.save()
        print(f"Superuser '{uname}' updated.")

# Create both with and without space
ensure_admin("Grad Admin", "admin@gradpulse.com", "GradP2026")
ensure_admin("GradAdmin", "admin2@gradpulse.com", "GradP2026")
