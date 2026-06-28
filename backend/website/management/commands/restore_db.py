"""Command to restore the database."""
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Restore the SQLite database from a backup file"

    def add_arguments(self, parser):
        parser.add_argument("backup", help="Path to the backup .sqlite3 file")

    def handle(self, *args, **options):
        src = Path(options["backup"])
        if not src.exists():
            self.stdout.write(self.style.ERROR(f"Backup not found: {src}"))
            return
        db_path = Path(settings.DATABASES["default"]["NAME"])
        db_path.write_bytes(src.read_bytes())
        self.stdout.write(self.style.SUCCESS(f"Restored database from {src}"))
