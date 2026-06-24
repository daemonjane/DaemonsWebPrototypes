from django.test import TestCase

class Suite401(TestCase):
    def test_basic(self):
        self.assertLess(401, 500)
