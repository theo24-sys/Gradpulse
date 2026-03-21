import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradpulse.settings')
django.setup()

print(f"RECAPTCHA_PUBLIC_KEY: {getattr(settings, 'RECAPTCHA_PUBLIC_KEY', 'NOT FOUND')}")
print(f"RECAPTCHA_PRIVATE_KEY: {getattr(settings, 'RECAPTCHA_PRIVATE_KEY', 'NOT FOUND')}")
