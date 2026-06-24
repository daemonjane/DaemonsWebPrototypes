from django.test import TestCase

class Suite323(TestCase):
    def test_basic(self):
        self.assertLess(323, 500)
