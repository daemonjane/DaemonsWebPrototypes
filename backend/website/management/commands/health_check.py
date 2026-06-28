"""Command to perform health check."""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Run a basic health check on the Django app."

    def handle(self, *args, **options):
        self.stdout.write("Checking database connection...", ending=" ")
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS("OK"))
        except Exception as e:
            self.stdout.write(self.style.ERROR("FAIL"))
            self.stdout.write(str(e))
            return
        self.stdout.write(self.style.SUCCESS("All systems operational."))
