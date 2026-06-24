from django.test import TestCase

class Suite380(TestCase):
    def test_basic(self):
        self.assertLess(380, 500)
