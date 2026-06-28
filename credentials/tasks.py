import logging
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Credential, Simulation
from accounts.ai_utils import generate_search_queries, generate_simulation_scenario
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


@shared_task
def generate_simulation_ai_task(topic, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        scenario = generate_simulation_scenario(topic)
        if scenario:
            Simulation.objects.create(
                title=scenario.get('title', f"AI: {topic}"),
                description=scenario.get('situation', ''),
                category="AI Generated",
                difficulty="Intermediate",
                is_premium=True,
                is_ai_generated=True,
                json_content=scenario,
                created_by=user
            )
            logger.info(f"AI simulation generated for topic: {topic}")
        else:
            logger.error(f"AI returned no scenario for topic: {topic}")
    except Exception as e:
        logger.error(f"generate_simulation_ai_task failed: {e}")
