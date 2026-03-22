from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class MicrosoftCredentialsScraper(BaseScraper):
    source_name = "Microsoft Credentials"
    source_type = "credentials"
    sector = "international"
    base_url = "https://learn.microsoft.com/en-us/credentials/browse/"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Microsoft Learn structure
        cards = soup.select('.card-content') or soup.find_all('div', class_='card')
        
        for card in cards:
            title_node = card.select_one('.card-title') or card.find('h3')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = card.find('a').get('href') if card.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': urljoin(self.base_url, link),
                'company': "Microsoft",
                'description': "Professional certification or credential from Microsoft.",
                'location': "Online",
                'job_type': "Certification"
            })
            
        return items

class CourseraCertificatesScraper(BaseScraper):
    source_name = "Coursera Professional Certificates"
    source_type = "credentials"
    sector = "international"
    base_url = "https://www.coursera.org/professional-certificates"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Coursera structure
        courses = soup.select('.cds-productCard-content') or soup.find_all('div', class_='rc-DesktopSearchCard')
        
        for course in courses:
            title_node = course.find('h3') or course.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, course.find('a').get('href')) if course.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': link,
                'company': "Coursera",
                'description': "Professional Certificate program on Coursera.",
                'location': "Online",
                'job_type': "Professional Certificate"
            })
            
        return items

class GoogleGrowScraper(BaseScraper):
    source_name = "Google Career Certificates"
    source_type = "credentials"
    sector = "international"
    base_url = "https://grow.google/intl/ssa-en/courses-and-tools/?category=career"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Google Grow structure
        items_list = soup.select('.course-tool-card') or soup.find_all('div', class_='card')
        
        for item in items_list:
            title_node = item.select_one('.card-title') or item.find('h4')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = item.find('a').get('href') if item.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': urljoin(self.base_url, link),
                'company': "Google",
                'description': "Career-focused certificate or tool from Google.",
                'location': "Online",
                'job_type': "Course/Tool"
            })
            
        return items

class LeadershipKEScraper(BaseScraper):
    source_name = "Leadership Kenya Training"
    source_type = "credentials"
    sector = "private"
    base_url = "https://leadership.co.ke/training/"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Local leadership training
        trainings = soup.select('.training-item') or soup.find_all('article')
        
        for t in trainings:
            title_node = t.find('h3') or t.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, t.find('a').get('href')) if t.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': link,
                'company': "Leadership Kenya",
                'description': "Leadership and professional development training.",
                'location': "Kenya",
                'job_type': "Training"
            })
            
        return items
