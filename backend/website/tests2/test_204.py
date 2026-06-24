from django.test import TestCase

class WebTest204(TestCase):
    def test_simple(self):
        self.assertIsNotNone(204)
