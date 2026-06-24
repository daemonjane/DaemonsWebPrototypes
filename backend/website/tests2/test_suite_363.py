from django.test import TestCase

class Suite363(TestCase):
    def test_basic(self):
        self.assertLess(363, 500)
