from django.test import TestCase

class Suite376(TestCase):
    def test_basic(self):
        self.assertLess(376, 500)
