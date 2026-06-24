from django.test import TestCase

class Suite419(TestCase):
    def test_basic(self):
        self.assertLess(419, 500)
