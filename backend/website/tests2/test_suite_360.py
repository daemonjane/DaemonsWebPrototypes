from django.test import TestCase

class Suite360(TestCase):
    def test_basic(self):
        self.assertLess(360, 500)
