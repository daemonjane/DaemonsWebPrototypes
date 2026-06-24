from django.test import TestCase

class Suite411(TestCase):
    def test_basic(self):
        self.assertLess(411, 500)
