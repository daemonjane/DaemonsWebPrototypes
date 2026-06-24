from django.test import TestCase

class WebTest123(TestCase):
    def test_simple(self):
        self.assertIsNotNone(123)
