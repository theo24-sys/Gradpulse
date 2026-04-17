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
                # Get dataset details to help with categorization
                dataset_info = client.dataset(ds_id).get()
                ds_name = (dataset_info.get('name') or dataset_info.get('label') or '').lower()
                
                # Mapping dataset keywords to source types
                ds_type_map = {
                    'cert': 'credentials',
                    'course': 'credentials',
                    'learn': 'credentials',
                    'event': 'events',
                    'workshop': 'events',
                    'job': 'opportunities',
                    'intern': 'opportunities',
                    'youth': 'youth_programs',
                    'empower': 'youth_programs',
                    'scholarship': 'scholarships',
                    'simulation': 'simulations',
                    'qualification': 'qualifications'
                }
                
                ds_inferred_type = None
                for kw, s_type in ds_type_map.items():
                    if kw in ds_name:
                        ds_inferred_type = s_type
                        break

                items = client.dataset(ds_id).list_items().items
                for item in items:
                    url = item.get('url') or item.get('link') or item.get('job_link')
                    if not url:
                        continue
                    
                    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()

                    # Determine source info
                    source_name = item.get('company') or item.get('source_name') or 'Apify Scraper'
                    title = item.get('title', 'Unknown Title')
                    
                    # Fuzzy match source_name against scraper class source_names
                    matched_type = None
                    for s_name, s_type in name_to_type.items():
                        # check if scraper source_name is in item company/source, or vice versa
                        if s_name.lower() in source_name.lower() or source_name.lower() in s_name.lower():
                            matched_type = s_type
                            break
                    
                    source_type = matched_type or ds_inferred_type or item.get('job_type') or item.get('source_type') or 'opportunities'
                    
                    if source_type not in [c[0] for c in ScrapedItem.SOURCE_TYPES]:
                        # maybe the title has clues
                        if 'course' in title.lower() or 'cert' in title.lower():
                            source_type = 'credentials'
                        elif 'event' in title.lower() or 'workshop' in title.lower():
                            source_type = 'events'
                        else:
                            source_type = 'opportunities'

                    existing = ScrapedItem.objects.filter(url_hash=url_hash).first()
                    if existing:
                        if existing.source_type != source_type:
                            existing.source_type = source_type
                            existing.save()
                        total_skipped += 1
                        continue
                    
                    ScrapedItem.objects.create(
                        source_name=source_name[:200],
                        source_type=source_type,
                        sector='private',
                        title=title[:500],
                        company=item.get('company', '')[:255],
                        location=item.get('location', '')[:255],
                        description=item.get('description', ''),
                        url=url,
                        url_hash=url_hash,
                        deadline=item.get('deadline'),
                        salary=item.get('salary', '')[:255],
                        job_type=item.get('job_type', '')[:255],
                        course_tags=scraper_util.get_course_tags(title, item.get('description', '')),
                        year_tags=scraper_util.get_year_tags(title, item.get('description', '')),
                        raw_data=item,
                        status='pending'
                    )
                    total_saved += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing dataset {ds_id}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Sync Complete! Saved {total_saved} items. Skipped {total_skipped} duplicates.'))
