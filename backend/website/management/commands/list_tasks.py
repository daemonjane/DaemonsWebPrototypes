from django.core.management.base import BaseCommand

from website.models import Task


class Command(BaseCommand):
    help = "List all tasks with their status and creation date."

    def handle(self, *args, **options):
        tasks = Task.objects.all()
        if not tasks:
            self.stdout.write("No tasks found.")
            return
        for t in tasks:
            status = "✓" if t.completed else "○"
            self.stdout.write(f"[{t.pk:>2}] {status} {t.title} ({t.created_at.date()})")
