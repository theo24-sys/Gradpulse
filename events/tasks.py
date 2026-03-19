import logging
from celery import shared_task
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from .models import Event
from django.core.files.base import ContentFile
import urllib.parse
from datetime import timedelta

logger = logging.getLogger(__name__)

@shared_task
def scrape_events():
    """
    Periodic task to scrape events from external directories.
    Currently uses placeholder selectors for demonstration.
    """
    logger.info("Starting events scraping task...")
    
    url = "https://example.com/events"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to fetch events from {url}")
            return
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example logic: finding all event cards
        event_cards = soup.find_all('div', class_='event-card')
        
        events_created = 0
        for card in event_cards[:10]: # Limit to 10 for demonstration
            title_elem = card.find('h3')
            title = title_elem.text.strip() if title_elem else "Untitled Event"
            
            desc_elem = card.find('p', class_='description')
            description = desc_elem.text.strip() if desc_elem else "No description available."
            
            location_elem = card.find('span', class_='location')
            location = location_elem.text.strip() if location_elem else "Online"
            is_virtual = 'online' in location.lower() or 'virtual' in location.lower()
            
            # Using current time + offset as placeholder for date parsing
            # In a real scenario, you'd parse card.find('time')
            event_date = timezone.now() + timedelta(days=7)
            
            link_elem = card.find('a', href=True)
            virtual_link = urllib.parse.urljoin(url, link_elem['href']) if link_elem else ""
            
            # Create or update event
            event, created = Event.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'date': event_date,
                    'location': location,
                    'is_virtual': is_virtual,
                    'virtual_link': virtual_link if is_virtual else "",
                }
            )
            if created:
                events_created += 1
                
        logger.info(f"Events scraping completed. Created {events_created} new events.")
        
    except Exception as e:
        logger.error(f"Error scraping events: {e}")
