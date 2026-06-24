from django.test import TestCase

class WebTest213(TestCase):
    def test_simple(self):
        self.assertIsNotNone(213)
