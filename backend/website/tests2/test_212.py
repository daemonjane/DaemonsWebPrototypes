from django.test import TestCase

class WebTest212(TestCase):
    def test_simple(self):
        self.assertIsNotNone(212)
