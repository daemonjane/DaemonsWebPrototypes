from django.test import TestCase

class Suite361(TestCase):
    def test_basic(self):
        self.assertLess(361, 500)
