from django.test import TestCase

class WebTest128(TestCase):
    def test_simple(self):
        self.assertIsNotNone(128)
