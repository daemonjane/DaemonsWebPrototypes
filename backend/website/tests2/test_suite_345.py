from django.test import TestCase

class Suite345(TestCase):
    def test_basic(self):
        self.assertLess(345, 500)
