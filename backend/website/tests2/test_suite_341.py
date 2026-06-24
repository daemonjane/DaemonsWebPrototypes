from django.test import TestCase

class Suite341(TestCase):
    def test_basic(self):
        self.assertLess(341, 500)
