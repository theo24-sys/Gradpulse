import os
import hashlib
from django.core.management.base import BaseCommand
from django.conf import settings
from scraping.models import ScrapedItem
from scraping.base_scraper import BaseScraper

try:
    from apify_client import ApifyClient
except ImportError:
    ApifyClient = None

class Command(BaseCommand):
    help = 'Syncs available datasets from Apify into GradPulse ScrapedItem database.'

    def add_arguments(self, parser):
        parser.add_argument('--dataset', type=str, help='Specific Dataset ID to sync')
        parser.add_argument('--limit', type=int, default=10, help='Number of recent datasets to check if no ID provided')

    def handle(self, *args, **options):
        apify_token = getattr(settings, 'APIFY_TOKEN', os.environ.get('APIFY_TOKEN'))
        if not apify_token or not ApifyClient:
            self.stdout.write(self.style.ERROR('APIFY_TOKEN not set or apify_client not installed.'))
            return

        client = ApifyClient(apify_token)
        dataset_id = options.get('dataset')
        limit = options.get('limit')

        dataset_ids = []
        if dataset_id:
            dataset_ids.append(dataset_id)
        else:
            self.stdout.write(f'Fetching latest {limit} datasets from Apify...')
            datasets_page = client.datasets().list(limit=limit, desc=True)
            for ds in datasets_page.items:
                dataset_ids.append(ds['id'])

        total_saved = 0
        total_skipped = 0

        # Instantiate a dummy scraper to access utility methods like get_course_tags
        scraper_util = BaseScraper()

        # Create a mapping from source_name to scraper
        import pkgutil
        import importlib
        from scraping import scrapers
        
        name_to_type = {}
        for _, block_name, _ in pkgutil.iter_modules(scrapers.__path__):
            mod = importlib.import_module(f'scraping.scrapers.{block_name}')
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseScraper) and attr != BaseScraper:
                    name_to_type[attr.source_name] = attr.source_type

        for ds_id in dataset_ids:
            self.stdout.write(f'Syncing dataset {ds_id}...')
            try:
                items = client.dataset(ds_id).list_items().items
                
                for item in items:
                    url = item.get('url')
                    if not url:
                        continue
                    
                    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
                    if ScrapedItem.objects.filter(url_hash=url_hash).exists():
                        total_skipped += 1
                        continue

                    # Determine source info (default to generic if missing)
                    source_name = item.get('company') or item.get('source_name') or 'Apify Scraper'
                    
                    source_type = name_to_type.get(source_name)
                    if not source_type:
                        source_type = item.get('job_type') or item.get('source_type') or 'opportunities'
                        
                    if source_type not in [c[0] for c in ScrapedItem.SOURCE_TYPES]:
                        source_type = 'opportunities'
                    
                    ScrapedItem.objects.create(
                        source_name=source_name[:200],
                        source_type=source_type,
                        sector='private',  # simplistic default
                        title=item.get('title', 'Unknown Title')[:500],
                        company=item.get('company', '')[:255],
                        location=item.get('location', '')[:255],
                        description=item.get('description', ''),
                        url=url,
                        url_hash=url_hash,
                        deadline=item.get('deadline'),
                        salary=item.get('salary', '')[:255],
                        job_type=item.get('job_type', '')[:255],
                        course_tags=scraper_util.get_course_tags(item.get('title', ''), item.get('description', '')),
                        year_tags=scraper_util.get_year_tags(item.get('title', ''), item.get('description', '')),
                        raw_data=item.get('raw_data', {}),
                        status='pending'
                    )
                    total_saved += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing dataset {ds_id}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Sync Complete! Saved {total_saved} items. Skipped {total_skipped} duplicates.'))
