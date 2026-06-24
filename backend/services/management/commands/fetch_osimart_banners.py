from django.core.management.base import BaseCommand, CommandError

from services.osimart import OsimartClient, OsimartError


class Command(BaseCommand):
    help = "Fetch banners from the Osimart API"

    def add_arguments(self, parser):
        parser.add_argument("--store-id", type=str, help="Override the store ID from .env")

    def handle(self, *args, **options):
        store_id = options.get("store_id")
        client = OsimartClient(store_id=store_id)

        if not client.store_id:
            raise CommandError(
                "No store ID set. Set OSIMART_STORE_ID in .env or pass --store-id."
            )

        self.stdout.write(f"Fetching banners for store {client.store_id}...")

        try:
            data = client.get_banners()
        except OsimartError as e:
            raise CommandError(str(e))

        self.stdout.write(self.style.SUCCESS(f"Got response:"))
        self.stdout.write(str(data))
