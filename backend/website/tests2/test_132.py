from django.test import TestCase

class WebTest132(TestCase):
    def test_simple(self):
        self.assertIsNotNone(132)
