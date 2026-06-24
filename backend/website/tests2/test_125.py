from django.test import TestCase

class WebTest125(TestCase):
    def test_simple(self):
        self.assertIsNotNone(125)
