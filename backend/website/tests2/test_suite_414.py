from django.test import TestCase

class Suite414(TestCase):
    def test_basic(self):
        self.assertLess(414, 500)
