from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class PostTrainingFairsScraper(BaseScraper):
    source_name = "Post Training Job Fairs"
    source_type = "events"
    sector = "government"
    base_url = "https://posttraining.go.ke/find-job-fairsevents"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Government job fairs
        fairs = soup.select('.event-list-item') or soup.find_all('div', class_='event')
        
        for fair in fairs:
            title_node = fair.find('h4') or fair.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, fair.find('a').get('href')) if fair.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': link,
                'company': "Government of Kenya",
                'description': "National job fair or career event.",
                'location': "Kenya (Various)",
                'job_type': "Job Fair"
            })
            
        return items

class AllConferenceAlertScraper(BaseScraper):
    source_name = "AllConferenceAlert Kenya"
    source_type = "events"
    sector = "private"
    base_url = "https://www.allconferencealert.com/kenya/career-fair"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Global conference alerts for Kenya
        rows = soup.select('.conf-list tr') or soup.find_all('tr')
        
        for row in rows[1:]: # Skip header
            cols = row.find_all('td')
            if len(cols) < 2: continue
            
            date = cols[0].get_text(strip=True)
            title_node = cols[1].find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, title_node.get('href'))
            
            items.append({
                'title': title,
                'url': link,
                'company': "International Conferences",
                'description': f"Career fair/conference on {date}.",
                'location': "Kenya",
                'job_type': "Conference"
            })
            
        return items

class NLBHEventsScraper(BaseScraper):
    source_name = "NLBH Events"
    source_type = "events"
    sector = "private"
    base_url = "https://nlbh.ke/events/"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Local Nairobi events
        event_cards = soup.select('.tribe-events-pro-photo__event-details') or soup.find_all('div', class_='tribe-events-calendar-list__event-details')
        
        for card in event_cards:
            title_node = card.select_one('.tribe-events-pro-photo__event-title a') or card.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, title_node.get('href'))
            
            items.append({
                'title': title,
                'url': link,
                'company': "Nairobi Events",
                'description': "Local networking or career-related event.",
                'location': "Nairobi, Kenya",
                'job_type': "Networking"
            })
            
        return items
