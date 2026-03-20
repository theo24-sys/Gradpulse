from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
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
                items.append({
                    'title': a.text.strip(),
                    'url': a['href'],
                    'description': art.find('p').text.strip() if art.find('p') else "",
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
        
        jobs = soup.find_all('article', class_='rw-river-article')
        for job in jobs:
            title_node = job.find('h3', class_='rw-river-article__title')
            if title_node and title_node.find('a'):
                a = title_node.find('a')
                items.append({
                    'title': a.text.strip(),
                    'url': "https://reliefweb.int" + a['href'] if a['href'].startswith('/') else a['href'],
                    'company': job.find('li', class_='rw-river-article__source').text.strip() if job.find('li', class_='rw-river-article__source') else "NGO",
                    'description': f"ReliefWeb job posting for Kenya",
                })
        return items
