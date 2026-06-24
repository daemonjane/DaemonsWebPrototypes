from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .models import Category, Product


class ImportVueDataTests(TestCase):
    def test_creates_products_and_categories(self):
        self.assertEqual(Product.objects.count(), 0)
        out = StringIO()
        call_command("import_vue_data", stdout=out)
        self.assertEqual(Product.objects.count(), 21)
        self.assertIn("21 products", out.getvalue())
        self.assertIn("21 created", out.getvalue())
        cats = set(Category.objects.values_list("slug", flat=True))
        self.assertIn("desktop", cats)
        self.assertIn("monitors", cats)
        self.assertIn("peripherals", cats)

    def test_updates_existing_products(self):
        cat = Category.objects.create(slug="peripherals", name="Peripherals")
        Product.objects.create(
            slug="cyberpro-keyboard",
            name="Old Name",
            price="50",
            category=cat,
            rating=0.0,
        )
        out = StringIO()
        call_command("import_vue_data", stdout=out)
        keyboard = Product.objects.get(slug="cyberpro-keyboard")
        self.assertEqual(keyboard.name, "Cyber-Pro Mechanical Keyboard")
        self.assertIn("21 products", out.getvalue())
        self.assertIn("20 created, 1 updated", out.getvalue())

    def test_idempotent(self):
        call_command("import_vue_data", stdout=StringIO())
        first = Product.objects.count()
        call_command("import_vue_data", stdout=StringIO())
        self.assertEqual(Product.objects.count(), first)
