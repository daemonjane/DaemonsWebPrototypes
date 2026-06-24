from django.test import TestCase

class Suite382(TestCase):
    def test_basic(self):
        self.assertLess(382, 500)
