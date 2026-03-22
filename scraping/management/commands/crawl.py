from django.core.management.base import BaseCommand
from scraping.scrapers.government import PSCKenyaScraper, AjiraDigitalScraper, NYSScraper, NYOTAProjectScraper
from scraping.scrapers.scholarships import ScholarshipPositionsScraper, ScholarshipSetScraper
from scraping.scrapers.ngos import UNKenyaScraper, ReliefWebScraper
from scraping.scrapers.opportunities_expanded import (
    BrighterMondayInternsScraper, MyJobMagInternsScraper, 
    LinkedInInternsScraper, CFKAfricaScraper, MultiWorkScraper
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
    EducationFairsAfricaScraper, ConferenceAlertsNairobiScraper
)

class Command(BaseCommand):
    help = 'Runs web scrapers by category or name'

    CATEGORIES = {
        'gov': [PSCKenyaScraper, AjiraDigitalScraper, NYSScraper, NYOTAProjectScraper],
        'ngos': [UNKenyaScraper, ReliefWebScraper, WorldVisionKenyaScraper, CapYEIScraper, GenerationKenyaScraper],
        'scholarships': [ScholarshipPositionsScraper, ScholarshipSetScraper],
        'jobs': [BrighterMondayInternsScraper, MyJobMagInternsScraper, LinkedInInternsScraper, CFKAfricaScraper, MultiWorkScraper],
        'learning': [MicrosoftCredentialsScraper, CourseraCertificatesScraper, GoogleGrowScraper, IBMTrainingScraper, ISACACredentialsScraper, ITCILOCoursesScraper, LeadershipKEScraper],
        'events': [PostTrainingFairsScraper, EducationFairsAfricaScraper, AllConferenceAlertScraper, NLBHEventsScraper, ConferenceAlertsNairobiScraper],
    }

    def add_arguments(self, parser):
        parser.add_argument('target', type=str, help='Category (gov, ngos, scholarships, jobs, learning, events) or "all"')

    def handle(self, *args, **options):
        target = options['target'].lower()

        # Aliases for better UX
        aliases = {
            'certs': 'learning',
            'credentials': 'learning',
            'certification': 'learning',
            'fairs': 'events',
            'networking': 'events',
            'government': 'gov',
            'internships': 'jobs',
        }
        
        target = aliases.get(target, target)

        if target == 'all':
            self.stdout.write(self.style.WARNING('🚀 Running ALL scrapers... This might take a while.'))
            for cat, scrapers in self.CATEGORIES.items():
                self.run_group(scrapers)
        elif target in self.CATEGORIES:
            self.stdout.write(self.style.SUCCESS(f'🔎 Running category: {target}'))
            self.run_group(self.CATEGORIES[target])
        else:
            self.stdout.write(self.style.ERROR(f'❌ Error: Category "{target}" not found.'))
            self.stdout.write(f'Valid categories: {", ".join(self.CATEGORIES.keys())} or "all"')

    def run_group(self, scrapers):
        for ScraperClass in scrapers:
            scraper = ScraperClass()
            self.stdout.write(f'--- Starting {scraper.source_name} ---')
            try:
                # Scraper.run() handles the Railway vs Local vs Apify logic
                scraper.run()
                self.stdout.write(self.style.SUCCESS(f'✅ Successfully triggered {scraper.source_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Failed {scraper.source_name}: {str(e)}'))
