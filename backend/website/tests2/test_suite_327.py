from django.test import TestCase

class Suite327(TestCase):
    def test_basic(self):
        self.assertLess(327, 500)
