from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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
        
        program_cards = soup.select('.training-card') or soup.select('.card')
        for card in program_cards:
            title_node = card.select_one('h3') or card.select_one('h4')
            if title_node:
                title = title_node.get_text(strip=True)
                link_node = card.select_one('a')
                url = urljoin(self.base_url, link_node['href']) if link_node else self.base_url
                
                desc_node = card.select_one('p')
                description = desc_node.get_text(strip=True) if desc_node else f"Training Program: {title}"
                
                items.append({
                    'title': title,
                    'url': url,
                    'description': description,
                    'company': "Ajira Digital",
                })
        return items

class MastercardFoundationScraper(BaseScraper):
    source_name = "Mastercard Foundation"
    source_type = "youth_programs"
    sector = "international"
    base_url = "https://mastercardfdn.org/all-programs"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        links = soup.select('a[href*="/all-programs/"]')
        for link in links:
            title = link.get_text(strip=True)
            if title:
                items.append({
                    'title': title,
                    'url': urljoin(self.base_url, link['href']),
                    'company': "Mastercard Foundation",
                    'description': f"Youth empowerment program by Mastercard Foundation: {title}"
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
            title = sec.get_text(strip=True)
            if title:
                items.append({
                    'title': title,
                    'url': self.base_url,
                    'company': "Youth Enterprise Development Fund",
                    'description': f"Government youth funding program: {title}"
                })
        return items
