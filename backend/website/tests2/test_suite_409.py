from django.test import TestCase

class Suite409(TestCase):
    def test_basic(self):
        self.assertLess(409, 500)
