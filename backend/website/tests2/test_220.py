from django.test import TestCase

class WebTest220(TestCase):
    def test_simple(self):
        self.assertIsNotNone(220)
