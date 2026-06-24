from django.test import TestCase

class Suite392(TestCase):
    def test_basic(self):
        self.assertLess(392, 500)
