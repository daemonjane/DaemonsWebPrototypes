from django.test import TestCase

class Suite321(TestCase):
    def test_basic(self):
        self.assertLess(321, 500)
