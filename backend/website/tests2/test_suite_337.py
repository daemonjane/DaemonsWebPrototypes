from django.test import TestCase

class Suite337(TestCase):
    def test_basic(self):
        self.assertLess(337, 500)
