from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class KenyaLawScraper(BaseScraper):
    source_name = "Kenya Law"
    source_type = "simulations"
    sector = "government"
    base_url = "https://kenyalaw.org/caselaw"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Case summaries
        cases = soup.select('.case-content') # Example selector
        for case in cases:
            title_node = case.find('h4')
            if title_node:
                items.append({
                    'title': title_node.text.strip(),
                    'url': self.base_url,
                    'description': case.find('p').text.strip() if case.find('p') else "Legal case summary for simulation seed",
                    'company': "Judiciary of Kenya",
                })
        return items

class CBKPressScraper(BaseScraper):
    source_name = "Central Bank of Kenya"
    source_type = "simulations"
    sector = "government"
    base_url = "https://www.centralbank.go.ke/press-releases"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        releases = soup.select('.press-release-item')
        for rel in releases:
            title_node = rel.find('h3')
            if title_node:
                items.append({
                    'title': title_node.text.strip(),
                    'url': rel.find('a')['href'] if rel.find('a') else self.base_url,
                    'description': "Financial news for economic simulation seed",
                    'company': "Central Bank of Kenya",
                })
        return items

class CMAScraper(BaseScraper):
    source_name = "CMA Kenya"
    source_type = "simulations"
    sector = "government"
    base_url = "https://www.cma.or.ke/index.php/enforcement-actions"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        rows = soup.select('table tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                items.append({
                    'title': f"Enforcement: {cols[0].text.strip()}",
                    'url': self.base_url,
                    'description': cols[1].text.strip(),
                    'company': "Capital Markets Authority",
                })
        return items
