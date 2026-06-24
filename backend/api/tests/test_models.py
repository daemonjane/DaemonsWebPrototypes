from django.test import TestCase

from api.models import Category, Product


class CategoryTest(TestCase):
    def test_create_category(self):
        c = Category.objects.create(name="Test", slug="test")
        self.assertEqual(str(c), "Test")


class ProductTest(TestCase):
    def test_create_product(self):
        c = Category.objects.create(name="Test", slug="test")
        p = Product.objects.create(slug="test-p", name="Test P", price=10, category=c, rating=4.0)
        self.assertEqual(str(p), "Test P")
