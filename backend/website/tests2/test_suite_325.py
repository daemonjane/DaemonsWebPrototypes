from django.test import TestCase

class Suite325(TestCase):
    def test_basic(self):
        self.assertLess(325, 500)
