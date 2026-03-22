from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class OpportunitiesForYoungKenyansScraper(BaseScraper):
    source_name = "Opportunities For Young Kenyans"
    source_type = "opportunities"
    sector = "private"
    base_url = "https://opportunitiesforyoungkenyans.co.ke/"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # This site is usually a blog-style listing
        articles = soup.select('article') or soup.find_all('article')
        
        for article in articles:
            title_node = article.select_one('h2.entry-title a') or article.find('h2').find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = title_node.get('href')
            
            items.append({
                'title': title,
                'url': link,
                'company': "Various",
                'description': "Opportunity for youth in Kenya.",
                'location': "Kenya",
                'job_type': "Internship/Job"
            })
            
        return items

class BrighterMondayInternsScraper(BaseScraper):
    source_name = "BrighterMonday Internships"
    source_type = "opportunities"
    sector = "private"
    base_url = "https://www.brightermonday.co.ke/jobs/internship-graduate"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # BrighterMonday structure
        job_listings = soup.select('.job-search-card') or soup.select('.w-full.flex.flex-col')
        
        for job in job_listings:
            title_node = job.select_one('h2 a') or job.find('a', class_='relative')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, title_node.get('href'))
            
            company_node = job.select_one('.job-search-card__company') or job.find('p', class_='text-sm')
            company = company_node.get_text(strip=True) if company_node else "Unknown"
            
            items.append({
                'title': title,
                'url': link,
                'company': company,
                'description': f"Internship/Graduate role at {company}.",
                'location': "Kenya",
                'job_type': "Internship"
            })
            
        return items

class MyJobMagInternsScraper(BaseScraper):
    source_name = "MyJobMag Nairobi Internships"
    source_type = "opportunities"
    sector = "private"
    base_url = "https://www.myjobmag.co.ke/cp/internship-opportunities-nairobi"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # MyJobMag structure
        job_list = soup.select('.job-info') or soup.find_all('li', class_='job-info')
        
        for job in job_list:
            title_node = job.select_one('h2 a') or job.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, title_node.get('href'))
            
            description = job.select_one('.job-details')
            desc_text = description.get_text(strip=True) if description else ""
            
            items.append({
                'title': title,
                'url': link,
                'company': "Various",
                'description': desc_text[:200],
                'location': "Nairobi, Kenya",
                'job_type': "Internship"
            })
            
        return items

class CFKAfricaScraper(BaseScraper):
    source_name = "CFK Africa Career"
    source_type = "opportunities"
    sector = "ngo"
    base_url = "https://cfkafrica.org/work-with-us/"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Specialized NGO careers page
        jobs = soup.select('.job-posting') or soup.find_all('div', class_='careers-list')
        
        for job in jobs:
            title_node = job.find('h3') or job.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = job.find('a').get('href') if job.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': urljoin(self.base_url, link),
                'company': "CFK Africa",
                'description': "NGO career opportunity.",
                'location': "Nairobi (Kibera), Kenya",
                'job_type': "NGO/Community Work"
            })
            
        return items
