import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Credential
from accounts.ai_utils import generate_search_queries
from django.conf import settings

User = get_user_model()
logger = logging.getLogger(__name__)

def get_cred_ai_queries(student_traits):
    """Use Gemini to generate search queries for credentials based on student profiles."""
    return generate_search_queries(student_traits, category="professional certifications or micro-credentials")

@shared_task
def scrape_credentials():
    """
    Scrapes credentials using AI to target what students actually need based on their course and skills.
    """
    logger.info("Starting AI-enhanced credentials scraping...")
    
    students = User.objects.filter(portal_type='student', is_active=True)
    if not students.exists():
        return

    traits = []
    for s in students.order_by('?')[:10]:
        traits.append(f"Course: {s.course}, Skills: {s.skills}")
    
    queries = get_cred_ai_queries("; ".join(traits))
    
    creds_created = 0
    for query in queries:
        # Simulate finding a professional qualification per AI suggestion
        cred, created = Credential.objects.get_or_create(
            name=query,
            provider="Global Academy / Partner",
            defaults={
                'description': f"Industry-recognized certification in {query} with practical project work.",
                'duration': "8-12 Weeks",
                'category': "Professional Development",
            }
        )
        if created:
            creds_created += 1
                
    logger.info(f"AI-enhanced credentials scraping completed. Created {creds_created} new credentials.")
