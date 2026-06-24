from django.test import TestCase

class Suite348(TestCase):
    def test_basic(self):
        self.assertLess(348, 500)
