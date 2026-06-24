from django.core.management.base import BaseCommand
from django.db import transaction

from website.models import ContactMessage, NewsletterSubscription


class Command(BaseCommand):
    help = "Anonymize personal data for GDPR/privacy compliance"

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=365, help="Anonymize records older than N days")

    @transaction.atomic
    def handle(self, *args, **options):
        from datetime import timedelta
        from django.utils import timezone
        cutoff = timezone.now() - timedelta(days=options["days"])
        old_messages = ContactMessage.objects.filter(created_at__lt=cutoff)
        count = old_messages.count()
        for msg in old_messages:
            msg.name = "[anonymized]"
            msg.email = f"anon{msg.pk}@example.com"
            msg.message = "[anonymized]"
            msg.save(update_fields=["name", "email", "message"])
        self.stdout.write(self.style.SUCCESS(f"Anonymized {count} old contact messages"))
