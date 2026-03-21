from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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
            title = a.get_text(strip=True)
            if not title: continue
            
            url = urljoin(self.base_url, a['href'])
            
            # Find parent container to look for company
            parent = a.find_parent('div')
            company = "Private Company"
            if parent:
                company_node = parent.select_one('p.text-sm') or parent.find('p', class_='text-sm')
                if not company_node:
                    company_node = a.find_next('p', class_='text-sm')
                
                if company_node:
                    company = company_node.get_text(strip=True)
            
            items.append({
                'title': title,
                'url': url,
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
        
        job_list = soup.select('li.job-list-item, div.job-info, .job-info-card')
        for job in job_list:
            h2 = job.find(['h2', 'h3'])
            if h2 and h2.find('a'):
                a = h2.find('a')
                title = a.get_text(strip=True)
                url = urljoin(self.base_url, a['href'])
                
                company_node = job.select_one('li.job-list-company') or job.find('li', class_='job-list-company')
                company = company_node.get_text(strip=True) if company_node else "Private Company"
                
                items.append({
                    'title': title,
                    'url': url,
                    'company': company,
                })
        return items

class FuzuScraper(BaseScraper):
    source_name = "Fuzu Kenya"
    source_type = "opportunities"
    sector = "private"
    base_url = "https://www.fuzu.com/kenya/jobs"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        cards = soup.select('a[href*="/kenya/job/"], .job-card')
        for card in cards:
            title_node = card.find(['h6', 'h5', 'h4', 'h3'])
            if title_node:
                title = title_node.get_text(strip=True)
                url = urljoin(self.base_url, card.get('href', ''))
                
                items.append({
                    'title': title,
                    'url': url,
                    'company': "Fuzu Partner",
                    'description': f"Job opportunity on Fuzu: {title}"
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
        links = soup.select('a[href*="taleo"], a[href*="career"]')
        for link in links:
            title = link.get_text(strip=True)
            if "career" in title.lower() or "job" in title.lower() or "vacancy" in title.lower():
                items.append({
                    'title': title,
                    'url': urljoin(self.base_url, link['href']),
                    'company': "Safaricom PLC",
                    'description': f"Career opportunity at Safaricom: {title}"
                })
        return items
