from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class PSCKenyaScraper(BaseScraper):
    source_name = "Public Service Commission Kenya"
    source_type = "opportunities"
    sector = "government"
    base_url = "https://www.publicservice.go.ke/index.php/careers"

    def parse(self):
        # PSC often requires JS rendering or has anti-bot that Apify handles better
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Use more targeted selector for the table
        table = soup.select_one('table') or soup.find('table')
        rows = table.select('tr') if table else soup.find_all('tr')

        for row in rows[1:]: # Skip header
            cols = row.find_all('td')
            if len(cols) >= 3:
                title_link = cols[1].find('a')
                if title_link:
                    title = title_link.get_text(strip=True)
                    url = urljoin(self.base_url, title_link['href'])
                    
                    items.append({
                        'title': title,
                        'url': url,
                        'description': cols[2].get_text(strip=True) if len(cols) > 2 else f"Public Service Commission Vacancy: {title}",
                        'company': "Public Service Commission",
                        'raw_data': {'column_data': [c.get_text(strip=True) for c in cols]}
                    })
        return items

class KRAScraper(BaseScraper):
    source_name = "Kenya Revenue Authority"
    source_type = "opportunities"
    sector = "government"
    base_url = "https://www.kra.go.ke/careers"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # KRA specific parsing
        anchors = soup.find_all('a', href=True)
        for a in anchors:
            if "career" in a['href'].lower() or "vacancy" in a['href'].lower():
                title = a.get_text(strip=True)
                if title and len(title) > 10:
                    items.append({
                        'title': title,
                        'url': urljoin(self.base_url, a['href']),
                        'description': f"KRA Career Opportunity: {title}",
                        'company': "Kenya Revenue Authority",
                    })
        return items

class KPLCScraper(BaseScraper):
    source_name = "Kenya Power"
    source_type = "opportunities"
    sector = "public"
    base_url = "https://www.kplc.co.ke/careers"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # KPLC specific parsing
        links = soup.select('a[href*="career"]')
        for link in links:
            title = link.get_text(strip=True)
            if title:
                items.append({
                    'title': title,
                    'url': urljoin(self.base_url, link['href']),
                    'description': f"Kenya Power Vacancy: {title}",
                    'company': "Kenya Power",
                })
        return items
