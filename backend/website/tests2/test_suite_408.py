from django.test import TestCase

class Suite408(TestCase):
    def test_basic(self):
        self.assertLess(408, 500)
