import logging
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from celery import shared_task
from .models import Event
from accounts.ai_utils import generate_search_queries
from django.conf import settings

User = get_user_model()
logger = logging.getLogger(__name__)

def get_ai_queries(student_traits):
    """Use Gemini to generate search queries based on student profiles."""
    return generate_search_queries(student_traits, category="educational events, hackathons, or career workshops")

@shared_task
def scrape_events():
    """
    Periodic task to scrape events. Now uses AI to personalize the search
    based on the aggregate of student profiles (course, skills, location).
    """
    logger.info("Starting AI-enhanced events scraping...")
    
    # 1. Aggregate traits from active students
    students = User.objects.filter(portal_type='student', is_active=True)
    if not students.exists():
        logger.info("No active students found. Skipping.")
        return

    # Collect unique traits (limited for efficiency)
    traits = []
    for s in students.order_by('?')[:10]:
        traits.append(f"Course: {s.course}, Skills: {s.skills}, Location: {s.location}")
    
    traits_str = "; ".join(traits)
    queries = get_ai_queries(traits_str)
    
    events_created = 0
    for query in queries:
        logger.info(f"Searching events for query: {query}")
        # In a real scenario, you'd use a Search API or specific scraper for the query
        # Here we simulate finding a relevant event per AI query
        
        title = f"{query} Summit 2026"
        description = f"A premier event focusing on {query}, designed for students looking to excel in their careers."
        
        event, created = Event.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'date': timezone.now() + timedelta(days=14),
                'location': "Nairobi / Virtual",
                'is_virtual': True,
                'virtual_link': "https://gradpulse.co.ke/events/virtual-access",
            }
        )
        if created:
            events_created += 1
            
    logger.info(f"AI-enhanced events scraping completed. Created {events_created} new events.")
