from django.test import TestCase

class Suite416(TestCase):
    def test_basic(self):
        self.assertLess(416, 500)
