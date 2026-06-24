from django.test import TestCase

class Suite329(TestCase):
    def test_basic(self):
        self.assertLess(329, 500)
