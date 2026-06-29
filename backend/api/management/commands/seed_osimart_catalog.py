"""Management command to seed Osimart catalog from JSON data files."""
from django.core.management.base import BaseCommand

from ..seed_data.loader import SeedLoader


class Command(BaseCommand):
    help = "Create categories, brands, variant types, collections, and products from seed_data/ JSON files"

    def handle(self, *args, **options):
        verbosity = int(options["verbosity"])
        loader = SeedLoader()
        loader.load_all(verbosity=verbosity)
        self.stdout.write(self.style.SUCCESS("Done seeding Osimart catalog."))
