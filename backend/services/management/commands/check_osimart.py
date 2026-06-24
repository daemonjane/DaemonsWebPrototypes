from django.core.management.base import BaseCommand

from services.osimart import OsimartClient, OsimartError


class Command(BaseCommand):
    help = "Check connectivity and data from the Osimart API"

    def handle(self, *args, **options):
        client = OsimartClient()
        try:
            store = client.get_store()
            self.stdout.write(self.style.SUCCESS(f"Store: {store.get('name', 'unknown')}"))
        except OsimartError as e:
            self.stdout.write(self.style.ERROR(f"Store error: {e}"))
        for name, method in [("products", "get_products"), ("categories", "get_categories"), ("brands", "get_brands"), ("banners", "get_banners")]:
            try:
                data = getattr(client, method)()
                count = data.get("count", len(data.get("results", data)))
                self.stdout.write(self.style.SUCCESS(f"{name}: {count} items"))
            except OsimartError as e:
                self.stdout.write(self.style.ERROR(f"{name}: {e}"))
