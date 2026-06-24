from django.test import TestCase

class Suite379(TestCase):
    def test_basic(self):
        self.assertLess(379, 500)
