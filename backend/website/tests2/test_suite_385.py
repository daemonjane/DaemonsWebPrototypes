from django.test import TestCase

class Suite385(TestCase):
    def test_basic(self):
        self.assertLess(385, 500)
