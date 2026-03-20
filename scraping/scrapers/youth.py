from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class AjiraDigitalScraper(BaseScraper):
    source_name = "Ajira Digital Kenya"
    source_type = "youth_programs"
    sector = "government"
    base_url = "https://ajiradigital.go.ke/training"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        program_cards = soup.select('.training-card') # Example selector
        for card in program_cards:
            title_node = card.find('h3')
            if title_node:
                items.append({
                    'title': title_node.text.strip(),
                    'url': self.base_url,
                    'description': card.find('p').text.strip() if card.find('p') else "Ajira Digital Training Program",
                    'company': "Ajira Digital",
                })
        return items

class MastercardFoundationScraper(BaseScraper):
    source_name = "Mastercard Foundation"
    source_type = "youth_programs"
    sector = "international"
    base_url = "https://mastercardfdn.org/all-programs"

    def parse(self):
        html = self.fetch_js(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        links = soup.select('a[href*="/all-programs/"]')
        for link in links:
            title = link.text.strip()
            if title:
                items.append({
                    'title': title,
                    'url': link['href'],
                    'company': "Mastercard Foundation",
                })
        return items

class YouthFundScraper(BaseScraper):
    source_name = "Youth Enterprise Development Fund"
    source_type = "youth_programs"
    sector = "government"
    base_url = "https://www.youthfund.go.ke/programmes"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        sections = soup.find_all('h3')
        for sec in sections:
            title = sec.text.strip()
            if title:
                items.append({
                    'title': title,
                    'url': self.base_url,
                    'company': "Youth Enterprise Development Fund",
                })
        return items
