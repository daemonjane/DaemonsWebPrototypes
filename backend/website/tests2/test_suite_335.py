from django.test import TestCase

class Suite335(TestCase):
    def test_basic(self):
        self.assertLess(335, 500)
