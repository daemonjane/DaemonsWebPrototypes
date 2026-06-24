from django.test import TestCase

class Suite374(TestCase):
    def test_basic(self):
        self.assertLess(374, 500)
