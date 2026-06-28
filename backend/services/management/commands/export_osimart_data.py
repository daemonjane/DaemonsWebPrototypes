"""Command to export Osimart data."""
import json

from django.core.management.base import BaseCommand

from services.osimart import OsimartClient, OsimartError


class Command(BaseCommand):
    help = "Export Osimart API data to JSON files"

    def add_arguments(self, parser):
        parser.add_argument("--dir", default="/tmp/osimart_export", help="Output directory")

    def handle(self, *args, **options):
        out_dir = options["dir"]
        from pathlib import Path
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        client = OsimartClient()
        endpoints = [
            ("products", "get_products"),
            ("categories", "get_categories"),
            ("brands", "get_brands"),
            ("banners", "get_banners"),
            ("collections", "get_collections"),
            ("store", "get_store"),
            ("home", "get_home"),
        ]
        for name, method_name in endpoints:
            try:
                data = getattr(client, method_name)()
                path = Path(out_dir) / f"{name}.json"
                path.write_text(json.dumps(data, indent=2, default=str))
                self.stdout.write(self.style.SUCCESS(f"Wrote {path}"))
            except OsimartError as e:
                self.stdout.write(self.style.ERROR(f"{name}: {e}"))
