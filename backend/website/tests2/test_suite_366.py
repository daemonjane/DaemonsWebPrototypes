from django.test import TestCase

class Suite366(TestCase):
    def test_basic(self):
        self.assertLess(366, 500)
