import httpx
import time
import random
import hashlib
import logging
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from django.utils import timezone
from .models import ScrapedItem, ScrapeLog
from urllib.parse import urljoin
import json
import re

logger = logging.getLogger(__name__)

class BaseScraper:
    source_name = ""
    source_type = ""
    sector = "private"
    base_url = ""

    def __init__(self):
        self.ua = UserAgent()
        self.log_entry = None

    def get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }

    def fetch_html(self, url):
        """Standard HTML fetch using httpx."""
        try:
            with httpx.Client(follow_redirects=True, timeout=30.0) as client:
                response = client.get(url, headers=self.get_headers())
                response.raise_for_status()
                return response.text
        except Exception as e:
            logger.error(f"HTTPX error fetching {url}: {e}")
            return None

    def fetch_js(self, url):
        """Fallback to fetch_html since Playwright is removed."""
        return self.fetch_html(url)

    def get_course_tags(self, title, description):
        """Keyword matching for courses."""
        courses = [
            "Computer Science", "Information Technology", "Business", "Finance", 
            "Accounting", "Engineering", "Law", "Medicine", "Nursing", "Marketing",
            "Human Resource", "Agriculture", "Procurement", "Economics", "Statistics",
            "Data Science", "Hospitality", "Social Work", "Communication"
        ]
        found = []
        text = f"{title} {description}".lower()
        for course in courses:
            if course.lower() in text:
                found.append(course)
        return found

    def get_year_tags(self, title, description):
        """Keyword matching for year levels."""
        tags = []
        text = f"{title} {description}".lower()
        if any(kw in text for kw in ["year 1", "first year", "1st year"]): tags.append(1)
        if any(kw in text for kw in ["year 2", "second year", "2nd year"]): tags.append(2)
        if any(kw in text for kw in ["year 3", "third year", "3rd year"]): tags.append(3)
        if any(kw in text for kw in ["year 4", "fourth year", "4th year", "final year", "graduating"]): tags.append(4)
        if "fresh graduate" in text or "entry level" in text: tags.extend([4])
        return list(set(tags))

    def save_item(self, data):
        """Saves a single item to the database after deduplication."""
        url = data.get('url')
        if not url: return False
        
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        if ScrapedItem.objects.filter(url_hash=url_hash).exists():
            return "skipped"

        try:
            ScrapedItem.objects.create(
                source_name=self.source_name,
                source_type=self.source_type,
                sector=self.sector,
                title=data.get('title'),
                company=data.get('company'),
                location=data.get('location'),
                description=data.get('description'),
                url=url,
                url_hash=url_hash,
                deadline=data.get('deadline'),
                salary=data.get('salary'),
                job_type=data.get('job_type'),
                course_tags=self.get_course_tags(data.get('title', ''), data.get('description', '')),
                year_tags=self.get_year_tags(data.get('title', ''), data.get('description', '')),
                raw_data=data.get('raw_data', {}),
                status='pending'
            )
            return "saved"
        except Exception as e:
            logger.error(f"Error saving item {url}: {e}")
            return "error"

    def run(self):
        """Main execution loop for the scraper."""
        self.log_entry = ScrapeLog.objects.create(
            source=self.source_name,
            status="started",
            started_at=timezone.now()
        )
        
        items_found = 0
        items_saved = 0
        items_skipped = 0
        error_msg = None

        try:
            scraped_data = self.parse()
            items_found = len(scraped_data)
            
            for item in scraped_data:
                res = self.save_item(item)
                if res == "saved": items_saved += 1
                elif res == "skipped": items_skipped += 1
                
                # Random delay
                time.sleep(random.uniform(2, 5))
                
            self.log_entry.status = "finished"
        except Exception as e:
            self.log_entry.status = "failed"
            error_msg = str(e)
            logger.error(f"Scraper {self.source_name} failed: {e}")

        self.log_entry.finished_at = timezone.now()
        self.log_entry.items_found = items_found
        self.log_entry.items_saved = items_saved
        self.log_entry.items_skipped = items_skipped
        self.log_entry.error_message = error_msg
        self.log_entry.save()

    def parse(self):
        """Overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement parse()")
