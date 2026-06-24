from django.test import TestCase

class WebTest135(TestCase):
    def test_simple(self):
        self.assertIsNotNone(135)
