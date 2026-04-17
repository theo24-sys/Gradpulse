from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class ScholarshipPositionsScraper(BaseScraper):
    source_name = "Scholarship Positions"
    source_type = "scholarships"
    sector = "international"
    base_url = "https://scholarship-positions.com/category/kenya-scholarships/"

    def parse(self):
        # Use cloud rendering
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Select scholarship posts
        posts = soup.select('article') or soup.select('.post')
        
        for post in posts:
            title_node = post.select_one('h2.entry-title a') or post.select_one('h2 a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = title_node.get('href')
            
            desc_node = post.select_one('.entry-content') or post.select_one('.post-content')
            description = desc_node.get_text(strip=True) if desc_node else ""
            
            # Simple metadata extraction
            items.append({
                'title': title,
                'url': link,
                'company': "Various",
                'description': description,
                'location': "Global/Kenya",
                'job_type': "Scholarship",
                'raw_data': {
                    'source': self.source_name,
                    'excerpt': description[:500]
                }
            })
            
        return items

class ScholarshipSetScraper(BaseScraper):
    source_name = "ScholarshipSet"
    source_type = "scholarships"
    sector = "international"
    base_url = "https://www.scholarshipset.com/scholarships-for-kenya"

    def parse(self):
        result = self.fetch_apify(self.base_url)
        if isinstance(result, list): return result
        
        html = result
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # Common structure for listing pages
        cards = soup.select('.scholarship-item') or soup.select('li.list-group-item')
        
        for card in cards:
            title_node = card.select_one('h3 a') or card.find('a')
            if not title_node: continue
            
            title = title_node.get_text(strip=True)
            link = urljoin(self.base_url, title_node.get('href'))
            
            items.append({
                'title': title,
                'url': link,
                'company': "International",
                'description': "Scholarship opportunity for Kenyan students.",
                'location': "Global",
                'job_type': "Scholarship"
            })
            
        return items
