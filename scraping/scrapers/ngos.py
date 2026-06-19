from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class UNKenyaScraper(BaseScraper):
    source_name = "UN Kenya"
    source_type = "opportunities"
    sector = "ngo"
    base_url = "https://kenya.un.org/en/jobs"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # UN Jobs are often in a list or table
        job_nodes = soup.select('.views-row') or soup.find_all('div', class_='job-item')
        
        for node in job_nodes:
            title_node = node.select_one('.field-name-title a') or node.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, title_node.get('href'))
            
            agency_node = node.select_one('.field-name-field-job-agency')
            agency = agency_node.get_text(strip=True) if agency_node else "United Nations"
            
            items.append({
                'title': title,
                'url': link,
                'company': agency,
                'description': "UN opportunity in Kenya.",
                'location': "Kenya",
                'job_type': "Contract/Internship"
            })
            
        return items

class ReliefWebScraper(BaseScraper):
    source_name = "ReliefWeb Kenya"
    source_type = "opportunities"
    sector = "ngo"
    base_url = "https://reliefweb.int/jobs?search=kenya+youth+internship"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # ReliefWeb search results
        cards = soup.select('article.rw-river-article')
        
        for card in cards:
            title_node = card.select_one('h4.rw-river-article__title a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, title_node.get('href'))
            
            org_node = card.select_one('.rw-river-article__source')
            org = org_node.get_text(strip=True) if org_node else "NGO"
            
            items.append({
                'title': title,
                'url': link,
                'company': org,
                'description': f"Opportunity via ReliefWeb by {org}",
                'location': "Kenya",
                'job_type': "NGO/Volunteer"
            })
            
        return items
