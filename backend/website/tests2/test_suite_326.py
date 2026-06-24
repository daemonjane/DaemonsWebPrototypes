from django.test import TestCase

class Suite326(TestCase):
    def test_basic(self):
        self.assertLess(326, 500)
