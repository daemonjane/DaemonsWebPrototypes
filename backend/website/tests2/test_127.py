from django.test import TestCase

class WebTest127(TestCase):
    def test_simple(self):
        self.assertIsNotNone(127)
