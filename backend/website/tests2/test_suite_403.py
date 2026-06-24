from django.test import TestCase

class Suite403(TestCase):
    def test_basic(self):
        self.assertLess(403, 500)
