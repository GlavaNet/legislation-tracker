from celery import Celery
from celery.schedules import crontab
from .scrapers.congress import CongressScraper
from .scrapers.federal_register import FederalRegisterScraper

celery = Celery('legislation_tracker',
                broker='redis://redis:6379/0',
                backend='redis://redis:6379/0')

@celery.task
def scrape_federal_legislation():
    with CongressScraper() as scraper:
        return scraper.scrape()

@celery.task
def scrape_executive_orders():
    with FederalRegisterScraper() as scraper:
        return scraper.scrape()

# Schedule tasks
celery.conf.beat_schedule = {
    'scrape-federal-every-hour': {
        'task': 'app.worker.scrape_federal_legislation',
        'schedule': crontab(minute=0)  # Run every hour
    },
    'scrape-executive-every-hour': {
        'task': 'app.worker.scrape_executive_orders',
        'schedule': crontab(minute=30)  # Run every hour at :30
    }
}
