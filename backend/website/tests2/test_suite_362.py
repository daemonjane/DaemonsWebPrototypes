from django.test import TestCase

class Suite362(TestCase):
    def test_basic(self):
        self.assertLess(362, 500)
