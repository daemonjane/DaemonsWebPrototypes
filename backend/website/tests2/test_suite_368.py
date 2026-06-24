from django.test import TestCase

class Suite368(TestCase):
    def test_basic(self):
        self.assertLess(368, 500)
