from django.test import TestCase

class Suite343(TestCase):
    def test_basic(self):
        self.assertLess(343, 500)
