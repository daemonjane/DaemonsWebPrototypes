from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Backup the SQLite database to a timestamped file"

    def add_arguments(self, parser):
        parser.add_argument("--out", help="Output path (default: db/backups/backup_<timestamp>.sqlite3)")

    def handle(self, *args, **options):
        db_path = settings.DATABASES["default"]["NAME"]
        src = Path(db_path)
        if not src.exists():
            self.stdout.write(self.style.ERROR(f"Database not found: {src}"))
            return
        out_path = options.get("out")
        if not out_path:
            backup_dir = Path(settings.BASE_DIR) / "db" / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = str(backup_dir / f"backup_{ts}.sqlite3")
        dest = Path(out_path)
        dest.write_bytes(src.read_bytes())
        self.stdout.write(self.style.SUCCESS(f"Backup saved to {dest} ({(dest.stat().st_size / 1024):.0f} KB)"))
