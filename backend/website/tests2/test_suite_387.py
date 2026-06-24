from django.test import TestCase

class Suite387(TestCase):
    def test_basic(self):
        self.assertLess(387, 500)
