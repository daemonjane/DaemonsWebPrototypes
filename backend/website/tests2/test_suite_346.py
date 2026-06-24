from django.test import TestCase

class Suite346(TestCase):
    def test_basic(self):
        self.assertLess(346, 500)
