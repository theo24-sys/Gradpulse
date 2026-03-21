from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class BrighterMondayScraper(BaseScraper):
    source_name = "BrighterMonday Kenya"
    source_type = "opportunities"
    sector = "private"
    base_url = "https://www.brightermonday.co.ke/jobs?q=internship&l=kenya"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Direct search for listing links
        links = soup.select('a[href*="/listings/"]')
        for a in links:
            title = a.text.strip()
            if not title: continue
            
            # Find parent container to look for company
            parent = a.find_parent('div')
            company = "Private Company"
            if parent:
                company_node = parent.find_next_sibling('p', class_='text-sm') or parent.find('p', class_='text-sm')
                if not company_node:
                    # Look globally near the link
                    company_node = a.find_next('p', class_='text-sm')
                
                if company_node:
                    company = company_node.text.strip()
            
            items.append({
                'title': title,
                'url': a['href'] if a['href'].startswith('http') else "https://www.brightermonday.co.ke" + a['href'],
                'company': company,
                'description': f"Internship listing from BrighterMonday",
            })
        return items

class MyJobMagScraper(BaseScraper):
    source_name = "MyJobMag Kenya"
    source_type = "opportunities"
    sector = "private"
    base_url = "https://www.myjobmag.co.ke/jobs-in-kenya"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        job_list = soup.select('li.job-list-item, div.job-info')
        for job in job_list:
            h2 = job.find(['h2', 'h3'])
            if h2 and h2.find('a'):
                a = h2.find('a')
                items.append({
                    'title': a.text.strip(),
                    'url': "https://www.myjobmag.co.ke" + a['href'] if a['href'].startswith('/') else a['href'],
                    'company': job.find('li', class_='job-list-company').text.strip() if job.find('li', class_='job-list-company') else "Private Company",
                })
        return items

class FuzuScraper(BaseScraper):
    source_name = "Fuzu Kenya"
    source_type = "opportunities"
    sector = "private"
    base_url = "https://www.fuzu.com/kenya/jobs"

    def parse(self):
        # Using standard fetch as Playwright is removed
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        cards = soup.select('a[href*="/kenya/job/"], .job-card')
        for card in cards:
            title_node = card.find(['h6', 'h5', 'h4', 'h3'])
            if title_node:
                items.append({
                    'title': title_node.text.strip(),
                    'url': "https://www.fuzu.com" + card['href'] if card['href'].startswith('/') else card['href'],
                    'company': "Fuzu Partner",
                })
        return items

class SafaricomScraper(BaseScraper):
    source_name = "Safaricom Careers"
    source_type = "opportunities"
    sector = "private"
    base_url = "https://www.safaricom.co.ke/careers"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Safaricom specific
        links = soup.select('a[href*="taleo"]')
        for link in links:
            if "career" in link.text.lower() or "job" in link.text.lower():
                items.append({
                    'title': link.text.strip(),
                    'url': link['href'],
                    'company': "Safaricom PLC",
                })
        return items
