from django.test import TestCase

class WebTest200(TestCase):
    def test_simple(self):
        self.assertIsNotNone(200)
