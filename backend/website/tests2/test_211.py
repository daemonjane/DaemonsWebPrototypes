from django.test import TestCase

class WebTest211(TestCase):
    def test_simple(self):
        self.assertIsNotNone(211)
