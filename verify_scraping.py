import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradpulse.settings')
django.setup()

from events.tasks import scrape_events
from credentials.tasks import scrape_credentials
from accounts.models import CustomUser
from events.models import Event
from credentials.models import Credential

# Create a test student with specific traits
user, _ = CustomUser.objects.get_or_create(username='scrapetest', email='scrape@test.com', portal_type='student')
user.course = "Computer Science"
user.skills = "Python, AI, Web Development"
user.location = "Nairobi"
user.save()

print("Running scrape_events...")
try:
    scrape_events()
    print("Events in DB:", Event.objects.count())
except Exception as e:
    print(f"Error in scrape_events: {e}")

print("Running scrape_credentials...")
try:
    scrape_credentials()
    print("Credentials in DB:", Credential.objects.count())
except Exception as e:
    print(f"Error in scrape_credentials: {e}")
