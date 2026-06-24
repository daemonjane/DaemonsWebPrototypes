from django.test import TestCase

class Suite415(TestCase):
    def test_basic(self):
        self.assertLess(415, 500)
