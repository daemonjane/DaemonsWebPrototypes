from django.test import TestCase

class WebTest201(TestCase):
    def test_simple(self):
        self.assertIsNotNone(201)
