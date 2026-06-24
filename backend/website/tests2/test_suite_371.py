from django.test import TestCase

class Suite371(TestCase):
    def test_basic(self):
        self.assertLess(371, 500)
