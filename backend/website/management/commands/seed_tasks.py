from django.core.management.base import BaseCommand

from website.models import Task

SEED_TASKS = [
    {"title": "Set up Django project structure", "description": "Create the Django project and website app", "completed": True},
    {"title": "Define and migrate models", "description": "Create Task and ContactMessage models", "completed": True},
    {"title": "Build homepage with Recent Tasks", "description": "Query and display latest tasks from database", "completed": True},
    {"title": "Add contact form feature", "description": "Form rendering, POST handling, validation, thank-you page", "completed": True},
    {"title": "Style Django sections", "description": "Match existing site styling with Tailwind classes", "completed": True},
    {"title": "Add authentication system", "description": "User login, registration, password reset", "completed": False},
    {"title": "Build product catalog", "description": "Display products from database with search and filter", "completed": False},
    {"title": "Implement shopping cart", "description": "Server-side cart with session persistence", "completed": False},
    {"title": "Add order management", "description": "Order tracking, history, admin management", "completed": False},
    {"title": "Deploy to production", "description": "Configure static files, database, and web server", "completed": False},
]


class Command(BaseCommand):
    help = "Seed the database with sample tasks"

    def handle(self, *args, **options):
        Task.objects.all().delete()
        for data in SEED_TASKS:
            Task.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(SEED_TASKS)} tasks"))
