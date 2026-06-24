from django.test import TestCase

class Suite357(TestCase):
    def test_basic(self):
        self.assertLess(357, 500)
