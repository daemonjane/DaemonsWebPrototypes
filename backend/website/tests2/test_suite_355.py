from django.test import TestCase

class Suite355(TestCase):
    def test_basic(self):
        self.assertLess(355, 500)
