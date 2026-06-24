from django.test import TestCase

class Suite349(TestCase):
    def test_basic(self):
        self.assertLess(349, 500)
