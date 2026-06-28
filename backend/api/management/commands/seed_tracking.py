"""Command to seed tracking/order data."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import Order, OrderTracking, TrackingHistory


class Command(BaseCommand):
    help = "Add sample tracking data to existing orders"

    def handle(self, *args, **options):
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stdout.write(self.style.WARNING("No admin user found. Run create_admin first."))
            return

        orders = Order.objects.filter(tracking__isnull=True)
        if not orders.exists():
            self.stdout.write(self.style.WARNING("No orders without tracking found."))
            return

        count = 0
        for order in orders:
            now = timezone.now()
            tracking = OrderTracking.objects.create(
                order=order,
                tracking_number=f"1Z{order.pk:07d}ABC{hash(order.email) % 10000:04d}",
                carrier="UPS",
                tracking_url="https://www.ups.com/track",
                estimated_delivery=(now + timedelta(days=3)).date(),
            )

            TrackingHistory.objects.create(
                tracking=tracking,
                status="Order Placed",
                location="Warehouse",
                timestamp=order.created_at,
            )
            TrackingHistory.objects.create(
                tracking=tracking,
                status="Processing",
                location="Distribution Center",
                timestamp=order.created_at + timedelta(hours=6),
            )
            TrackingHistory.objects.create(
                tracking=tracking,
                status="Picked Up",
                location="Sorting Facility",
                timestamp=order.created_at + timedelta(days=1),
            )
            TrackingHistory.objects.create(
                tracking=tracking,
                status="In Transit",
                location="Regional Hub",
                timestamp=order.created_at + timedelta(days=2),
            )

            if order.status in ("shipped", "out_for_delivery", "delivered"):
                TrackingHistory.objects.create(
                    tracking=tracking,
                    status="Out for Delivery",
                    location="Local Facility",
                    timestamp=now - timedelta(hours=2),
                )

            if order.status == "delivered":
                TrackingHistory.objects.create(
                    tracking=tracking,
                    status="Delivered",
                    location=order.address.split(",")[0].strip(),
                    note="Left at front door",
                    timestamp=now - timedelta(hours=1),
                )
                tracking.delivered_at = now - timedelta(hours=1)
                tracking.save()

            count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded tracking data for {count} order(s)"))
