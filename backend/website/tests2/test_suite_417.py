from django.test import TestCase

class Suite417(TestCase):
    def test_basic(self):
        self.assertLess(417, 500)
