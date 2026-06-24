from django.test import TestCase

class Suite364(TestCase):
    def test_basic(self):
        self.assertLess(364, 500)
