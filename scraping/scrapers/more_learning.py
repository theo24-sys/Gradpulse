from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class ISACACredentialsScraper(BaseScraper):
    source_name = "ISACA Credentialing"
    source_type = "credentials"
    sector = "international"
    base_url = "https://www.isaca.org/credentialing"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # ISACA certifications
        certs = soup.select('.card') or soup.find_all('div', class_='card-body')
        
        for cert in certs:
            title_node = cert.find('h3') or cert.find('h4')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = cert.find('a').get('href') if cert.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': urljoin(self.base_url, link),
                'company': "ISACA",
                'description': "IT Governance, Risk and Security certification.",
                'location': "Online/Global",
                'job_type': "Certification"
            })
            
        return items

class IBMTrainingScraper(BaseScraper):
    source_name = "IBM Training Certs"
    source_type = "credentials"
    sector = "international"
    # Scrapes both training and certifications
    targets = [
        "https://www.ibm.com/training/credentials",
        "https://www.ibm.com/training/credentials/certifications"
    ]

    def parse(self):
        items = []
        for url in self.targets:
            result = self.fetch_apify(url)
            if isinstance(result, list): 
                items.extend(result)
                continue
            
            html = result
            if not html: continue
            
            soup = BeautifulSoup(html, 'lxml')
            cards = soup.select('.ibm--card--content') or soup.find_all('div', class_='ibm-card')
            
            for card in cards:
                title_node = card.find('h3') or card.find('a')
                if not title_node: continue
                
                title = title_node.get_text(strip=True)
                items.append({
                    'title': title,
                    'url': url,
                    'company': "IBM",
                    'description': "IBM Professional Training or Certification.",
                    'location': "Online",
                    'job_type': "Professional Cert"
                })
        return items

class ITCILOCoursesScraper(BaseScraper):
    source_name = "ITCILO Courses"
    source_type = "credentials"
    sector = "international"
    base_url = "https://www.itcilo.org/courses"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # ITCILO courses for professional development
        courses = soup.select('.course-item') or soup.find_all('div', class_='views-row')
        
        for course in courses:
            title_node = course.find('h3') or course.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, course.find('a').get('href')) if course.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': link,
                'company': "ITCILO",
                'description': "International training center courses.",
                'location': "Online/Global",
                'job_type': "Training Course"
            })
            
        return items
