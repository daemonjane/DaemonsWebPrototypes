from django.test import TestCase

class Suite399(TestCase):
    def test_basic(self):
        self.assertLess(399, 500)
