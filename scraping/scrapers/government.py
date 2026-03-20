from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class PSCKenyaScraper(BaseScraper):
    source_name = "Public Service Commission Kenya"
    source_type = "opportunities"
    sector = "government"
    base_url = "https://www.publicservice.go.ke/index.php/vacancies"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Example parsing logic for PSC (Note: specific selectors depend on current site HTML)
        # Using a generic table/row approach as most gov sites use tables
        rows = soup.find_all('tr')
        for row in rows[1:]: # Skip header
            cols = row.find_all('td')
            if len(cols) >= 3:
                title_link = cols[1].find('a')
                if title_link:
                    title = title_link.text.strip()
                    url = title_link['href']
                    if not url.startswith('http'):
                        url = "https://www.publicservice.go.ke" + url
                    
                    items.append({
                        'title': title,
                        'url': url,
                        'description': f"Public Service Commission Vacancy: {title}",
                        'company': "Public Service Commission",
                        'raw_data': {'column_data': [c.text.strip() for c in cols]}
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
                title = a.text.strip()
                if title and len(title) > 10:
                    items.append({
                        'title': title,
                        'url': a['href'],
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
            title = link.text.strip()
            if title:
                items.append({
                    'title': title,
                    'url': link['href'],
                    'description': f"Kenya Power Vacancy: {title}",
                    'company': "Kenya Power",
                })
        return items
