from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class NGOJobsKenyaScraper(BaseScraper):
    source_name = "NGO Jobs Kenya"
    source_type = "opportunities"
    sector = "ngo"
    base_url = "https://www.ngojobskenya.com"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Standard blog/list type parsing
        articles = soup.find_all('article')
        for art in articles:
            h2 = art.find('h2')
            if h2 and h2.find('a'):
                a = h2.find('a')
                title = a.get_text(strip=True)
                url = urljoin(self.base_url, a['href'])
                
                desc_node = art.find('p')
                description = desc_node.get_text(strip=True) if desc_node else ""
                
                items.append({
                    'title': title,
                    'url': url,
                    'description': description,
                    'company': "Various NGOs",
                })
        return items

class ReliefWebScraper(BaseScraper):
    source_name = "ReliefWeb Kenya"
    source_type = "opportunities"
    sector = "ngo"
    base_url = "https://reliefweb.int/jobs?source=0&country=105"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        jobs = soup.select('article.rw-river-article')
        for job in jobs:
            title_node = job.select_one('h3.rw-river-article__title a')
            if title_node:
                title = title_node.get_text(strip=True)
                url = urljoin(self.base_url, title_node['href'])
                
                source_node = job.select_one('li.rw-river-article__source')
                company = source_node.get_text(strip=True) if source_node else "NGO"
                
                items.append({
                    'title': title,
                    'url': url,
                    'company': company,
                    'description': f"ReliefWeb job posting for Kenya",
                })
        return items
