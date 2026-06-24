from django.test import TestCase

class Suite402(TestCase):
    def test_basic(self):
        self.assertLess(402, 500)
