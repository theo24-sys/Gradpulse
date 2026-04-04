from ..base_scraper import BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class KASNEBScraper(BaseScraper):
    source_name = "KASNEB"
    source_type = "qualifications"
    sector = "government"
    base_url = "https://www.kasneb.or.ke/examinations/exam-timetable"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        # KASNEB timetable links
        links = soup.select('a[href*=".pdf"]')
        for link in links:
            title = link.text.strip()
            if "timetable" in title.lower():
                items.append({
                    'title': f"KASNEB Exam: {title}",
                    'url': link['href'],
                    'company': "KASNEB",
                })
        return items

class ICPAKScraper(BaseScraper):
    source_name = "ICPAK"
    source_type = "qualifications"
    sector = "private"
    base_url = "https://www.icpak.com/membership/student-registration"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        sections = soup.find_all(['h2', 'h3'])
        for sec in sections:
            title = sec.text.strip()
            if "student" in title.lower():
                items.append({
                    'title': title,
                    'url': self.base_url,
                    'company': "ICPAK",
                })
        return items

class ACCAKenyaScraper(BaseScraper):
    source_name = "ACCA Kenya"
    source_type = "qualifications"
    sector = "international"
    base_url = "https://www.accaglobal.com/ke/en/student.html"

    def parse(self):
        html = self.fetch_html(self.base_url)
        if not html: return []
        
        soup = BeautifulSoup(html, 'lxml')
        items = []
        
        links = soup.select('a.list-group-item')
        for link in links:
            title = link.text.strip()
            if title:
                items.append({
                    'title': f"ACCA: {title}",
                    'url': "https://www.accaglobal.com" + link['href'] if link['href'].startswith('/') else link['href'],
                    'company': "ACCA Global",
                })
        return items
