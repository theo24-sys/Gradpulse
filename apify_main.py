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
        from scraping.scrapers.government import (
            PSCKenyaScraper, AjiraDigitalScraper, NYSScraper, 
            NYOTAProjectScraper, YouthEmpowermentCentresScraper
        )
        from scraping.scrapers.events import EventbriteScraper, MeetupScraper
        from scraping.scrapers.private import BrighterMondayScraper
        from scraping.scrapers.scholarships import ScholarshipPositionsScraper, ScholarshipSetScraper
        from scraping.scrapers.ngos import UNKenyaScraper, ReliefWebScraper
        from scraping.scrapers.opportunities_expanded import (
            OpportunitiesForYoungKenyansScraper, BrighterMondayInternsScraper, 
            MyJobMagInternsScraper, CFKAfricaScraper, LinkedInInternsScraper, MultiWorkScraper
        )
        from scraping.scrapers.learning_expanded import (
            MicrosoftCredentialsScraper, CourseraCertificatesScraper, 
            GoogleGrowScraper, LeadershipKEScraper
        )
        from scraping.scrapers.events_multi import (
            PostTrainingFairsScraper, AllConferenceAlertScraper, NLBHEventsScraper
        )
        from scraping.scrapers.other_opportunities import (
            WorldVisionKenyaScraper, CapYEIScraper, GenerationKenyaScraper
        )
        from scraping.scrapers.more_learning import (
            ISACACredentialsScraper, IBMTrainingScraper, ITCILOCoursesScraper
        )
        from scraping.scrapers.more_events import (
            EducationFairsAfricaScraper, ConferenceAlertsNairobiScraper, 
            InternationalConferenceAlertsScraper
        )
        
        scrapers = {
            'PSCKenyaScraper': PSCKenyaScraper,
            'AjiraDigitalScraper': AjiraDigitalScraper,
            'NYSScraper': NYSScraper,
            'NYOTAProjectScraper': NYOTAProjectScraper,
            'YouthEmpowermentCentresScraper': YouthEmpowermentCentresScraper,
            'EventbriteScraper': EventbriteScraper,
            'MeetupScraper': MeetupScraper,
            'BrighterMondayScraper': BrighterMondayScraper,
            'ScholarshipPositionsScraper': ScholarshipPositionsScraper,
            'ScholarshipSetScraper': ScholarshipSetScraper,
            'UNKenyaScraper': UNKenyaScraper,
            'ReliefWebScraper': ReliefWebScraper,
            'OpportunitiesForYoungKenyansScraper': OpportunitiesForYoungKenyansScraper,
            'BrighterMondayInternsScraper': BrighterMondayInternsScraper,
            'MyJobMagInternsScraper': MyJobMagInternsScraper,
            'CFKAfricaScraper': CFKAfricaScraper,
            'LinkedInInternsScraper': LinkedInInternsScraper,
            'MultiWorkScraper': MultiWorkScraper,
            'MicrosoftCredentialsScraper': MicrosoftCredentialsScraper,
            'CourseraCertificatesScraper': CourseraCertificatesScraper,
            'GoogleGrowScraper': GoogleGrowScraper,
            'LeadershipKEScraper': LeadershipKEScraper,
            'PostTrainingFairsScraper': PostTrainingFairsScraper,
            'AllConferenceAlertScraper': AllConferenceAlertScraper,
            'NLBHEventsScraper': NLBHEventsScraper,
            'WorldVisionKenyaScraper': WorldVisionKenyaScraper,
            'CapYEIScraper': CapYEIScraper,
            'GenerationKenyaScraper': GenerationKenyaScraper,
            'ISACACredentialsScraper': ISACACredentialsScraper,
            'IBMTrainingScraper': IBMTrainingScraper,
            'ITCILOCoursesScraper': ITCILOCoursesScraper,
            'EducationFairsAfricaScraper': EducationFairsAfricaScraper,
            'ConferenceAlertsNairobiScraper': ConferenceAlertsNairobiScraper,
            'InternationalConferenceAlertsScraper': InternationalConferenceAlertsScraper,
        }
        
        if scraper_name not in scrapers:
            await Actor.fail(f"Scraper {scraper_name} not found!")
            return
            
        scraper_class = scrapers[scraper_name]
        instance = scraper_class()
        
        # We run the scraper in a separate thread to avoid asyncio loop conflicts 
        # with Playwright Sync API.
        try:
            import asyncio
            items = await asyncio.to_thread(instance.parse)
            print(f"Scraped {len(items)} items.")
            await Actor.push_data(items)
        except Exception as e:
            await Actor.fail(f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
