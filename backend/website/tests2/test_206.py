from django.test import TestCase

class WebTest206(TestCase):
    def test_simple(self):
        self.assertIsNotNone(206)
