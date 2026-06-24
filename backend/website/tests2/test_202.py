from django.test import TestCase

class WebTest202(TestCase):
    def test_simple(self):
        self.assertIsNotNone(202)
