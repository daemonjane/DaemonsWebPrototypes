"""
Management command to seed categories, brands, and variant types into Osimart.
"""
from django.core.management.base import BaseCommand
from services.osimart import OsimartClient, OsimartError


class Command(BaseCommand):
    help = "Create sample categories, brands, and variant types in Osimart"

    def handle(self, *args, **options):
        client = OsimartClient()
        verbosity = int(options["verbosity"])

        self._seed_categories(client, verbosity)
        self._seed_brands(client, verbosity)
        self._seed_variant_types(client, verbosity)

        self.stdout.write(self.style.SUCCESS("Done seeding Osimart catalog."))

    def _seed_categories(self, client, verbosity):
        categories = [
            {"name": "Desktops", "icon": "🖥️", "description": "Complete desktop systems"},
            {"name": "Monitors", "icon": "🖥️", "description": "Displays and monitors"},
            {"name": "Keyboards", "icon": "⌨️", "description": "Mechanical and membrane keyboards"},
            {"name": "Mice", "icon": "🖱️", "description": "Gaming and productivity mice"},
            {"name": "Audio", "icon": "🎧", "description": "Headsets, speakers, and microphones"},
            {"name": "Components", "icon": "🔧", "description": "Internal PC components"},
            {"name": "Accessories", "icon": "📦", "description": "Cables, mats, and peripherals"},
            {"name": "Furniture", "icon": "🪑", "description": "Desks, chairs, and stands"},
            {"name": "Networking", "icon": "🌐", "description": "Routers, switches, and adapters"},
            {"name": "Streaming", "icon": "📹", "description": "Stream decks, cameras, and lights"},
        ]
        for cat in categories:
            try:
                result = client.create_category(cat)
                if verbosity >= 1:
                    self.stdout.write(f"  ✓ Category '{cat['name']}' → {result.get('id', 'ok')}")
            except OsimartError as e:
                self.stdout.write(self.style.WARNING(f"  ✗ Category '{cat['name']}': {e}"))

    def _seed_brands(self, client, verbosity):
        brands = [
            {"name": "Vanguard", "description": "Premium performance hardware"},
            {"name": "CyberPro", "description": "Professional-grade peripherals"},
            {"name": "OptiView", "description": "High-fidelity display solutions"},
            {"name": "SonicWave", "description": "Audio engineering for creators"},
            {"name": "CableCraft", "description": "Custom cable solutions"},
            {"name": "ApexGear", "description": "Competitive gaming equipment"},
            {"name": "CoolFlow", "description": "Thermal management solutions"},
            {"name": "PowerCore", "description": "Reliable power and charging"},
        ]
        for brand in brands:
            try:
                result = client.create_brand(brand)
                if verbosity >= 1:
                    self.stdout.write(f"  ✓ Brand '{brand['name']}' → {result.get('id', 'ok')}")
            except OsimartError as e:
                self.stdout.write(self.style.WARNING(f"  ✗ Brand '{brand['name']}': {e}"))

    def _seed_variant_types(self, client, verbosity):
        variants = [
            {"name": "Color", "values": ["Black", "White", "Silver", "Gunmetal", "Red", "Blue", "Pink"]},
            {"name": "Size", "values": ["Small", "Medium", "Large", "XL"]},
            {"name": "Switch Type", "values": ["Linear", "Tactile", "Clicky"]},
            {"name": "Layout", "values": ["60%", "65%", "TKL", "Full Size"]},
            {"name": "Resolution", "values": ["1080p", "1440p", "4K"]},
            {"name": "Refresh Rate", "values": ["60Hz", "120Hz", "144Hz", "165Hz", "240Hz"]},
            {"name": "Capacity", "values": ["256GB", "512GB", "1TB", "2TB", "4TB"]},
            {"name": "Connectivity", "values": ["USB-C", "USB-A", "Bluetooth", "WiFi", "HDMI", "DisplayPort"]},
        ]
        for vt in variants:
            try:
                result = client.create_variant_type(vt)
                if verbosity >= 1:
                    self.stdout.write(f"  ✓ Variant '{vt['name']}' → {result.get('id', 'ok')}")
            except OsimartError as e:
                self.stdout.write(self.style.WARNING(f"  ✗ Variant '{vt['name']}': {e}"))
