from django.test import TestCase

class WebTest140(TestCase):
    def test_simple(self):
        self.assertIsNotNone(140)
