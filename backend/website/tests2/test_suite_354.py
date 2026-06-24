from django.test import TestCase

class Suite354(TestCase):
    def test_basic(self):
        self.assertLess(354, 500)
