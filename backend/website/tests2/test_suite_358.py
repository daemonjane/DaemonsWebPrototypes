from django.test import TestCase

class Suite358(TestCase):
    def test_basic(self):
        self.assertLess(358, 500)
