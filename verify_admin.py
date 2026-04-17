import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gradpulse.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

target_username = "Grad Admin"
user = User.objects.filter(username=target_username).first()

if user:
    print(f"User: {user.username}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")
    print(f"Is Active: {user.is_active}")
    print(f"Portal Type: {user.portal_type}")
    print(f"Password Check: {user.check_password('GradP2026')}")
else:
    print(f"User '{target_username}' not found!")

# Try without space just in case
user_no_space = User.objects.filter(username="GradAdmin").first()
if user_no_space:
    print(f"User No Space: {user_no_space.username}")
    print(f"Password Check No Space: {user_no_space.check_password('GradP2026')}")
