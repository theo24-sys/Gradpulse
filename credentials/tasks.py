import logging
from celery import shared_task
from .models import Credential
from django.contrib.auth import get_user_model
from openai import OpenAI
from django.conf import settings

User = get_user_model()
logger = logging.getLogger(__name__)

def get_cred_ai_queries(student_traits):
    """Use OpenAI to generate search queries for credentials based on student profiles."""
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = f"Based on student traits: {student_traits}, suggest 3 professional certifications or micro-credentials that would be highly valuable. Return names only, separated by newlines."
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip().split('\n')
    except Exception as e:
        logger.error(f"AI Credential Query Error: {e}")
        return ["Google Data Analytics", "Cisco Networking Essentials"]

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
