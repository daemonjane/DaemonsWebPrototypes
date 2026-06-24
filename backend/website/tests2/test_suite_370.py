from django.test import TestCase

class Suite370(TestCase):
    def test_basic(self):
        self.assertLess(370, 500)
