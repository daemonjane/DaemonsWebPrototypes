from django.test import TestCase

class WebTest210(TestCase):
    def test_simple(self):
        self.assertIsNotNone(210)
