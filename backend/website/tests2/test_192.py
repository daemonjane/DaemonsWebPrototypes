from django.test import TestCase

class WebTest192(TestCase):
    def test_simple(self):
        self.assertIsNotNone(192)
