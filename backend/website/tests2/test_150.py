from django.test import TestCase

class WebTest150(TestCase):
    def test_simple(self):
        self.assertIsNotNone(150)
