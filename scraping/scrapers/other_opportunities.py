from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class WorldVisionKenyaScraper(BaseScraper):
    source_name = "World Vision Kenya Youth"
    source_type = "youth_programs"
    sector = "ngo"
    base_url = "https://www.wvi.org/kenya/kenya-youth-economic-empowerment-program-kyeep"

    def parse(self):
        # FAST-FETCH: World Vision is usually static
        result = self.fetch_html(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # WV often uses h2 or cards for programs
        programs = soup.select('.views-row') or soup.find_all('div', class_='program-item')
        
        for program in programs:
            title_node = program.find('h3') or program.find('h2')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            items.append({
                'title': title,
                'url': self.base_url,
                'company': "World Vision Kenya",
                'description': "Youth economic empowerment opportunity.",
                'location': "Kenya",
                'job_type': "Youth Program"
            })
            
        return items

class CapYEIScraper(BaseScraper):
    source_name = "CAP Youth Empowerment Institute"
    source_type = "youth_programs"
    sector = "ngo"
    base_url = "https://capyei.org/"

    def parse(self):
        # FAST-FETCH: This site is notoriously slow in Playwright/Apify
        result = self.fetch_html(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Programs or news and events
        news = soup.select('.news-item') or soup.select('.post')
        
        for item in news:
            title_node = item.find('h4') or item.find('h3')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, item.find('a').get('href')) if item.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': link,
                'company': "CAP YEI",
                'description': "Youth vocational training or empowerment program.",
                'location': "Kenya",
                'job_type': "Vocational Training"
            })
            
        return items

class GenerationKenyaScraper(BaseScraper):
    source_name = "Generation Kenya Careers"
    source_type = "opportunities"
    sector = "ngo"
    base_url = "https://kenya.generation.org/find-a-career/"

    def parse(self):
        # FAST-FETCH
        result = self.fetch_html(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Programs / Courses listing
        programs = soup.select('.program-card') or soup.find_all('div', class_='program')
        
        for p in programs:
            title_node = p.find('h3') or p.find('h4')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, p.find('a').get('href')) if p.find('a') else self.base_url
            
            items.append({
                'title': title,
                'url': link,
                'company': "Generation Kenya",
                'description': "Skill-building program for employment.",
                'location': "Kenya (Various)",
                'job_type': "Skill Program"
            })
            
        return items
