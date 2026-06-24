from django.test import TestCase

class Suite373(TestCase):
    def test_basic(self):
        self.assertLess(373, 500)
