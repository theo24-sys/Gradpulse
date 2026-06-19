from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class EducationFairsAfricaScraper(BaseScraper):
    source_name = "Education Fairs Africa"
    source_type = "events"
    sector = "private"
    base_url = "https://educationfairsafrica.co.ke/"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Education fairs listing
        events = soup.select('.event') or soup.find_all('article')
        
        for event in events:
            title_node = event.find('h3') or event.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, event.find('a').get('href')) if event.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': link,
                'company': "Education Fairs Africa",
                'description': "Nairobi/Kenya education and career fair.",
                'location': "Kenya",
                'job_type': "Education Fair"
            })
            
        return items

class ConferenceAlertsNairobiScraper(BaseScraper):
    source_name = "Nairobi Networking Events"
    source_type = "events"
    sector = "private"
    base_url = "https://conferencealerts.co.in/nairobi/networking"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Table of conferences
        rows = soup.find_all('tr')
        
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) < 2: continue
            
            title_node = cols[1].find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, title_node.get('href'))
            
            items.append({
                'title': title,
                'url': link,
                'company': "Professional Conferences",
                'description': "Networking event or professional conference in Nairobi.",
                'location': "Nairobi, Kenya",
                'job_type': "Networking"
            })
            
        return items

class InternationalConferenceAlertsScraper(BaseScraper):
    source_name = "International Conferences Nairobi"
    source_type = "events"
    sector = "international"
    base_url = "https://internationalconferencealerts.com/conferences/nairobi"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # International conference listings
        cards = soup.select('.conf-list-item') or soup.find_all('div', class_='event-list')
        
        for card in cards:
            title_node = card.find('h3') or card.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, card.find('a').get('href')) if card.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': link,
                'company': "International Org",
                'description': "International conference in Nairobi.",
                'location': "Nairobi, Kenya",
                'job_type': "Conference"
            })
            
        return items
