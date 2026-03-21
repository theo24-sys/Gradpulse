from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class EventbriteScraper(BaseScraper):
    source_name = "Eventbrite Kenya"
    source_type = "events"
    sector = "private"
    base_url = "https://www.eventbrite.com/d/kenya/events"

    def parse(self):
        # Eventbrite is highly reactive and requires JS
        html = self.fetch_apify(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        events = soup.find_all('div', class_='event-card')
        for ev in events:
            h3 = ev.find('h3')
            link = ev.find('a', href=True)
            if h3 and link:
                items.append({
                    'title': h3.text.strip(),
                    'url': link['href'],
                    'location': ev.find('p', class_='event-card__location').text.strip() if ev.find('p', class_='event-card__location') else "Kenya",
                    'description': f"Event listing from Eventbrite Kenya",
                })
        return items

class MeetupScraper(BaseScraper):
    source_name = "Meetup Nairobi Tech"
    source_type = "events"
    sector = "private"
    base_url = "https://www.meetup.com/find/?location=Nairobi&categoryId=546"

    def parse(self):
        # Meetup uses JS for list rendering
        html = self.fetch_apify(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Specific Meetup card selectors
        cards = soup.select('a[id*="event-card-"]')
        for card in cards:
            title_node = card.find('h3')
            if title_node:
                items.append({
                    'title': title_node.text.strip(),
                    'url': card['href'] if card['href'].startswith('http') else "https://www.meetup.com" + card['href'],
                    'description': "Tech meetup in Nairobi",
                })
        return items

class IHubScraper(BaseScraper):
    source_name = "iHub Nairobi"
    source_type = "events"
    sector = "private"
    base_url = "https://ihub.co.ke/events"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        event_links = soup.select('.event-card a')
        for link in event_links:
            title_node = link.find('h4')
            if title_node:
                items.append({
                    'title': title_node.text.strip(),
                    'url': "https://ihub.co.ke" + link['href'] if link['href'].startswith('/') else link['href'],
                    'description': "Innovation and tech event at iHub Nairobi",
                })
        return items
