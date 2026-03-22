import httpx
import time
import random
import hashlib
import logging
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from django.utils import timezone
from .models import ScrapedItem, ScrapeLog
from urllib.parse import urljoin
import re
from django.conf import settings

try:
    from apify_client import ApifyClient
except ImportError:
    ApifyClient = None

logger = logging.getLogger(__name__)

class BaseScraper:
    source_name = ""
    source_type = ""
    sector = "private"
    base_url = ""

    def __init__(self):
        self.ua = UserAgent()
        self.log_entry = None
        self.apify_token = getattr(settings, 'APIFY_TOKEN', os.environ.get('APIFY_TOKEN'))
        self.apify_client = ApifyClient(self.apify_token) if self.apify_token and ApifyClient else None

    def fetch_js(self, url):
        """Fetch content using a real browser. Preferred to run on Apify."""
        if os.environ.get('APIFY_IS_AT_HOME'):
            try:
                # When running inside an Apify actor, we can use Playwright
                # (assuming it's installed in the actor environment)
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    # Relax wait_until to 'load' and increase timeout to 90s for heavy sites like IBM
                    page.goto(url, wait_until="load", timeout=90000)
                    content = page.content()
                    browser.close()
                    return content
            except Exception as e:
                logger.error(f"Playwright error on Apify: {e}")

        # Fallback to standard fetch if not on Apify or failed
        return self.fetch_html(url)

    def fetch_apify(self, url=None, actor=None):
        """
        Railway-side: Call Apify actor to get data.
        Apify-side: Perform JS fetch locally.
        """
        # 1. If we are ALREADY on Apify, don't call Apify again! (Avoid recursion)
        if os.environ.get('APIFY_IS_AT_HOME'):
            return self.fetch_js(url) if url else None

        # 2. On Railway: Call the actor
        if not self.apify_client:
            logger.warning("Apify client not initialized. Falling back to HTTPX.")
            return self.fetch_html(url) if url else None

        try:
            target_actor = actor or getattr(settings, 'APIFY_ACTOR', 'kingly_nomination/gradpulse')
            print(f"Railway: Delegating {self.__class__.__name__} to Apify actor {target_actor}...")

            run_input = { "scraper": self.__class__.__name__, "url": url }
            run = self.apify_client.actor(target_actor).call(run_input=run_input)

            # Retrieve results from the dataset
            dataset_items = self.apify_client.dataset(run["defaultDatasetId"]).list_items().items
            return dataset_items # This is a list of results
        except Exception as e:
            logger.error(f"Apify delegation error: {e}")
            return self.fetch_html(url) if url else None
        return None

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
