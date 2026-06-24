from django.core.management.base import BaseCommand

from api.models import Subscription

SUBSCRIPTIONS = [
    {
        "tier": "basic",
        "name": "Basic",
        "price": "9.99",
        "description": "Essential membership with exclusive deals and early access.",
        "features": [
            "Exclusive member deals",
            "Early access to drops",
            "Priority email support",
            "Monthly newsletter",
        ],
        "duration_days": 30,
    },
    {
        "tier": "pro",
        "name": "Pro",
        "price": "19.99",
        "description": "Enhanced membership with free shipping and extended warranty.",
        "features": [
            "Everything in Basic",
            "Free shipping on all orders",
            "Extended 2-year warranty",
            "VIP customer support",
            "Member-only Discord",
        ],
        "duration_days": 30,
    },
    {
        "tier": "enterprise",
        "name": "Enterprise",
        "price": "49.99",
        "description": "Premium tier with dedicated account manager and bulk pricing.",
        "features": [
            "Everything in Pro",
            "Dedicated account manager",
            "Bulk pricing discounts",
            "Custom build consultations",
            "White-glove setup service",
            "API access for inventory",
            "Quarterly hardware briefing",
        ],
        "duration_days": 30,
    },
]


class Command(BaseCommand):
    help = "Seed the database with subscription tiers"

    def handle(self, *args, **options):
        for data in SUBSCRIPTIONS:
            Subscription.objects.update_or_create(
                tier=data["tier"],
                defaults=data,
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(SUBSCRIPTIONS)} subscription tiers"))
