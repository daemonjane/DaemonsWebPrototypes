"""Command to count model instances."""
from django.core.management.base import BaseCommand

from website.models import Comment, ContactMessage, Task


class Command(BaseCommand):
    help = "Print a count of all website models."

    def handle(self, *args, **options):
        counts = {
            "Tasks": Task.objects.count(),
            "Comments": Comment.objects.count(),
            "Contact Messages": ContactMessage.objects.count(),
        }
        for label, count in counts.items():
            self.stdout.write(f"{label}: {count}")
