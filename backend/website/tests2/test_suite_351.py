from django.test import TestCase

class Suite351(TestCase):
    def test_basic(self):
        self.assertLess(351, 500)
