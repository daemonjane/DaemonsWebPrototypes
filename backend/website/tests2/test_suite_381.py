from django.test import TestCase

class Suite381(TestCase):
    def test_basic(self):
        self.assertLess(381, 500)
