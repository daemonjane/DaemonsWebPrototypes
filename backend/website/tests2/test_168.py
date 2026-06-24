from django.test import TestCase

class WebTest168(TestCase):
    def test_simple(self):
        self.assertIsNotNone(168)
