import os
import django
import sys
import json
from apify import Actor

async def main():
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        scraper_name = actor_input.get('scraper', 'PSCKenyaScraper')

        print(f"Starting scraper: {scraper_name}")

        # Setup Django (needed for models)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradpulse.settings')
        django.setup()

        # Dynamic import of the scraper
        from scraping.scrapers.government import PSCKenyaScraper
        from scraping.scrapers.events import EventbriteScraper, MeetupScraper
        from scraping.scrapers.private import BrighterMondayScraper
        
        scrapers = {
            'PSCKenyaScraper': PSCKenyaScraper,
            'EventbriteScraper': EventbriteScraper,
            'MeetupScraper': MeetupScraper,
            'BrighterMondayScraper': BrighterMondayScraper,
        }
        
        if scraper_name not in scrapers:
            await Actor.fail(f"Scraper {scraper_name} not found!")
            return
            
        scraper_class = scrapers[scraper_name]
        instance = scraper_class()
        
        # We override parse to return data instead of saving to DB 
        # (since this instance won't have the Railway DB access easily)
        # Actually, we can just run parse() and output to dataset.
        try:
            items = instance.parse()
            print(f"Scraped {len(items)} items.")
            await Actor.push_data(items)
        except Exception as e:
            await Actor.fail(f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
