from django.core.management.base import BaseCommand
from scraping.scrapers.government import PSCKenyaScraper, KRAScraper, KPLCScraper
from scraping.scrapers.ngo import NGOJobsKenyaScraper, ReliefWebScraper
from scraping.scrapers.private import BrighterMondayScraper, MyJobMagScraper, FuzuScraper, SafaricomScraper
from scraping.scrapers.events import EventbriteScraper, MeetupScraper, IHubScraper
from scraping.scrapers.youth import AjiraDigitalScraper, MastercardFoundationScraper, YouthFundScraper
from scraping.scrapers.credentials import GoogleDigitalSkillsScraper, MicrosoftLearnScraper, CiscoNetAcadScraper
from scraping.scrapers.qualifications import KASNEBScraper, ICPAKScraper, ACCAKenyaScraper
from scraping.scrapers.simulations import KenyaLawScraper, CBKPressScraper, CMAScraper

class Command(BaseCommand):
    help = "Run specified scrapers or all by default"

    def add_arguments(self, parser):
        parser.add_argument('--source', type=str, help='Specific scraper source name or category')

    def handle(self, *args, **options):
        source = options.get('source')
        
        scrapers = {
            # Map by name
            'Public Service Commission Kenya': PSCKenyaScraper,
            'Kenya Revenue Authority': KRAScraper,
            'Kenya Power': KPLCScraper,
            'NGO Jobs Kenya': NGOJobsKenyaScraper,
            'ReliefWeb Kenya': ReliefWebScraper,
            'BrighterMonday Kenya': BrighterMondayScraper,
            'MyJobMag Kenya': MyJobMagScraper,
            'Fuzu Kenya': FuzuScraper,
            'Safaricom Careers': SafaricomScraper,
            'Eventbrite Kenya': EventbriteScraper,
            'Meetup Nairobi Tech': MeetupScraper,
            'iHub Nairobi': IHubScraper,
            'Ajira Digital Kenya': AjiraDigitalScraper,
            'Mastercard Foundation': MastercardFoundationScraper,
            'Youth Enterprise Development Fund': YouthFundScraper,
            'Google Digital Skills for Africa': GoogleDigitalSkillsScraper,
            'Microsoft Learn': MicrosoftLearnScraper,
            'Cisco Networking Academy': CiscoNetAcadScraper,
            'KASNEB': KASNEBScraper,
            'ICPAK': ICPAKScraper,
            'ACCA Kenya': ACCAKenyaScraper,
            'Kenya Law': KenyaLawScraper,
            'Central Bank of Kenya': CBKPressScraper,
            'CMA Kenya': CMAScraper,
            
            # Map by category
            'opportunities': [PSCKenyaScraper, KRAScraper, KPLCScraper, NGOJobsKenyaScraper, ReliefWebScraper, BrighterMondayScraper, MyJobMagScraper, FuzuScraper, SafaricomScraper],
            'events': [EventbriteScraper, MeetupScraper, IHubScraper],
            'youth_programs': [AjiraDigitalScraper, MastercardFoundationScraper, YouthFundScraper],
            'credentials': [GoogleDigitalSkillsScraper, MicrosoftLearnScraper, CiscoNetAcadScraper],
            'qualifications': [KASNEBScraper, ICPAKScraper, ACCAKenyaScraper],
            'simulations': [KenyaLawScraper, CBKPressScraper, CMAScraper],
        }

        to_run = []
        if source:
            if source in scrapers:
                val = scrapers[source]
                if isinstance(val, list): to_run.extend(val)
                else: to_run.append(val)
            else:
                self.stdout.write(self.style.ERROR(f"Source '{source}' not found."))
                return
        else:
            # Run all categories
            for cat in ['opportunities', 'events', 'youth_programs', 'credentials', 'qualifications', 'simulations']:
                to_run.extend(scrapers[cat])

        self.stdout.write(f"Starting {len(to_run)} scrapers...")
        for scraper_cls in to_run:
            self.stdout.write(f"Running {scraper_cls.source_name}...")
            scraper = scraper_cls()
            scraper.run()
            self.stdout.write(self.style.SUCCESS(f"Finished {scraper_cls.source_name}"))

        self.stdout.write(self.style.SUCCESS("All tasks completed."))
