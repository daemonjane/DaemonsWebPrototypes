from django.test import TestCase

class WebTest180(TestCase):
    def test_simple(self):
        self.assertIsNotNone(180)
