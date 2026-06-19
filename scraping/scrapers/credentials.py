from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class GoogleDigitalSkillsScraper(BaseScraper):
    source_name = "Google Digital Skills for Africa"
    source_type = "credentials"
    sector = "private"
    base_url = "https://learndigital.withgoogle.com/digitalskills"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        courses = soup.select('.course-card')
        for course in courses:
            title_node = course.find('h3')
            if title_node:
                items.append({
                    'title': title_node.text.strip(),
                    'url': self.base_url,
                    'company': "Google",
                    'description': "Digital skills training for the African market",
                })
        return items

class MicrosoftLearnScraper(BaseScraper):
    source_name = "Microsoft Learn"
    source_type = "credentials"
    sector = "private"
    base_url = "https://learn.microsoft.com/en-us/training/browse/"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        cards = soup.select('div.card')
        for card in cards:
            h3 = card.find('h3')
            if h3:
                items.append({
                    'title': h3.text.strip(),
                    'url': "https://learn.microsoft.com" + card.find('a')['href'] if card.find('a') else self.base_url,
                    'company': "Microsoft",
                })
        return items

class CiscoNetAcadScraper(BaseScraper):
    source_name = "Cisco Networking Academy"
    source_type = "credentials"
    sector = "private"
    base_url = "https://www.netacad.com/courses/all"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        courses = soup.select('.course-tile')
        for course in courses:
            title = course.get('data-title') or course.text.strip()
            if title:
                items.append({
                    'title': title,
                    'url': self.base_url,
                    'company': "Cisco",
                })
        return items
