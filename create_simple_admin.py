import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gradpulse.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Create a very simple admin for fallback
uname = "admin"
pwd = "admin123"
if not User.objects.filter(username=uname).exists():
    user = User.objects.create_superuser(uname, "admin@example.com", pwd)
    user.portal_type = 'employer'
    user.save()
    print(f"Superuser '{uname}' created.")
else:
    user = User.objects.get(username=uname)
    user.set_password(pwd)
    user.save()
    print(f"Superuser '{uname}' updated.")
