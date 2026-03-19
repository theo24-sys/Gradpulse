import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradpulse.settings')
django.setup()

from django.test import Client
from accounts.models import CustomUser

try:
    user, _ = CustomUser.objects.get_or_create(username='teststudent', email='test@test.com', portal_type='student')
    user.set_password('password')
    user.save()

    client = Client()
    client.force_login(user)
    
    print("Fetching /campus/dashboard/")
    response = client.get('/campus/dashboard/')
    print('Status Code:', response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
