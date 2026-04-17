from celery import shared_task
from .scrapers.government import PSCKenyaScraper, KRAScraper, KPLCScraper
from .scrapers.ngo import NGOJobsKenyaScraper, ReliefWebScraper
from .scrapers.private import BrighterMondayScraper, MyJobMagScraper, FuzuScraper, SafaricomScraper
from .scrapers.events import EventbriteScraper, MeetupScraper, IHubScraper
from .scrapers.youth import AjiraDigitalScraper, MastercardFoundationScraper, YouthFundScraper
from .scrapers.credentials import GoogleDigitalSkillsScraper, MicrosoftLearnScraper, CiscoNetAcadScraper
from .scrapers.qualifications import KASNEBScraper, ICPAKScraper, ACCAKenyaScraper
from .scrapers.simulations import KenyaLawScraper, CBKPressScraper, CMAScraper

@shared_task(bind=True, max_retries=3)
def run_scraper_task(self, scraper_name):
    scrapers = {
        'PSCKenyaScraper': PSCKenyaScraper,
        'KRAScraper': KRAScraper,
        'KPLCScraper': KPLCScraper,
        'NGOJobsKenyaScraper': NGOJobsKenyaScraper,
        'ReliefWebScraper': ReliefWebScraper,
        'BrighterMondayScraper': BrighterMondayScraper,
        'MyJobMagScraper': MyJobMagScraper,
        'FuzuScraper': FuzuScraper,
        'SafaricomScraper': SafaricomScraper,
        'EventbriteScraper': EventbriteScraper,
        'MeetupScraper': MeetupScraper,
        'IHubScraper': IHubScraper,
        'AjiraDigitalScraper': AjiraDigitalScraper,
        'MastercardFoundationScraper': MastercardFoundationScraper,
        'YouthFundScraper': YouthFundScraper,
        'GoogleDigitalSkillsScraper': GoogleDigitalSkillsScraper,
        'MicrosoftLearnScraper': MicrosoftLearnScraper,
        'CiscoNetAcadScraper': CiscoNetAcadScraper,
        'KASNEBScraper': KASNEBScraper,
        'ICPAKScraper': ICPAKScraper,
        'ACCAKenyaScraper': ACCAKenyaScraper,
        'KenyaLawScraper': KenyaLawScraper,
        'CBKPressScraper': CBKPressScraper,
        'CMAScraper': CMAScraper,
    }
    
    if scraper_name in scrapers:
        scraper = scrapers[scraper_name]()
        try:
            scraper.run()
        except Exception as exc:
            raise self.retry(exc=exc, countdown=60)

@shared_task
def run_all_scrapers():
    run_opportunity_scrapers.delay()
    run_event_scrapers.delay()
    run_youth_program_scrapers.delay()
    run_credential_scrapers.delay()
    run_qualification_scrapers.delay()
    run_simulation_scrapers.delay()

@shared_task
def run_opportunity_scrapers():
    for name in ['PSCKenyaScraper', 'KRAScraper', 'KPLCScraper', 'NGOJobsKenyaScraper', 'ReliefWebScraper', 'BrighterMondayScraper', 'MyJobMagScraper', 'FuzuScraper', 'SafaricomScraper']:
        run_scraper_task.delay(name)

@shared_task
def run_event_scrapers():
    for name in ['EventbriteScraper', 'MeetupScraper', 'IHubScraper']:
        run_scraper_task.delay(name)

@shared_task
def run_youth_program_scrapers():
    for name in ['AjiraDigitalScraper', 'MastercardFoundationScraper', 'YouthFundScraper']:
        run_scraper_task.delay(name)

@shared_task
def run_credential_scrapers():
    for name in ['GoogleDigitalSkillsScraper', 'MicrosoftLearnScraper', 'CiscoNetAcadScraper']:
        run_scraper_task.delay(name)

@shared_task
def run_qualification_scrapers():
    for name in ['KASNEBScraper', 'ICPAKScraper', 'ACCAKenyaScraper']:
        run_scraper_task.delay(name)

@shared_task
def run_simulation_scrapers():
    for name in ['KenyaLawScraper', 'CBKPressScraper', 'CMAScraper']:
        run_scraper_task.delay(name)
