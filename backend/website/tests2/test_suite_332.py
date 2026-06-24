from django.test import TestCase

class Suite332(TestCase):
    def test_basic(self):
        self.assertLess(332, 500)
