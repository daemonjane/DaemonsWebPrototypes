from django.core.management.base import BaseCommand

from website.models import Task


class Command(BaseCommand):
    help = "Delete all tasks and reseed with sample data."

    def handle(self, *args, **options):
        Task.objects.all().delete()
        samples = [
            "Set up Django project structure",
            "Build homepage with Recent Tasks",
            "Add contact form feature",
            "Implement shopping cart",
            "Add order management",
            "Add authentication system",
            "Build product catalog",
            "CRUD Test Task",
        ]
        for title in samples:
            Task.objects.create(title=title)
        self.stdout.write(f"Reset: {Task.objects.count()} tasks created.")
