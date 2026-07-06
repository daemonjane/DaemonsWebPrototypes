"""Command to seed initial data."""
from django.core.management.base import BaseCommand

from api.models import ProductAddon


ADDONS = [
    {"product_slug": "gaming-mouse", "name": "Extra Glide Skates", "description": "Replacement PTFE glide skates", "price": "5.99"},
    {"product_slug": "gaming-mouse", "name": "Paracord Cable", "description": "Lightweight braided paracord cable", "price": "9.99"},
    {"product_slug": "gaming-mouse", "name": "Grip Tape Set", "description": "Textured grip tape for sides and buttons", "price": "3.99"},
]


class Command(BaseCommand):
    help = "Seed the database with add-ons linked to product slugs"

    def handle(self, *args, **options):
        addon_count = 0
        for addon_data in ADDONS:
            ProductAddon.objects.update_or_create(
                product_slug=addon_data["product_slug"],
                name=addon_data["name"],
                defaults={"description": addon_data["description"], "price": addon_data["price"]},
            )
            addon_count += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {addon_count} product add-ons"))
