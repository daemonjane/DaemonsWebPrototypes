from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a default admin superuser"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@techstore.dev", "admin123")
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created (password: admin123)"))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' already exists"))
