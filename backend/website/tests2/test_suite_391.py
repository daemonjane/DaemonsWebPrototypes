from django.test import TestCase

class Suite391(TestCase):
    def test_basic(self):
        self.assertLess(391, 500)
