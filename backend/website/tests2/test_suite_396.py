from django.test import TestCase

class Suite396(TestCase):
    def test_basic(self):
        self.assertLess(396, 500)
