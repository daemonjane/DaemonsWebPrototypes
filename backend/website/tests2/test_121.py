from django.test import TestCase

class WebTest121(TestCase):
    def test_simple(self):
        self.assertIsNotNone(121)
