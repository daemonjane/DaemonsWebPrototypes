from django.test import TestCase

class Suite356(TestCase):
    def test_basic(self):
        self.assertLess(356, 500)
