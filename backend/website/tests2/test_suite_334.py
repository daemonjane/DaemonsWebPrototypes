from django.test import TestCase

class Suite334(TestCase):
    def test_basic(self):
        self.assertLess(334, 500)
