from django.test import TestCase

class Suite365(TestCase):
    def test_basic(self):
        self.assertLess(365, 500)
