from django.test import TestCase

class Suite383(TestCase):
    def test_basic(self):
        self.assertLess(383, 500)
