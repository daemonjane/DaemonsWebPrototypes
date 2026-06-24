from django.test import TestCase

class Suite386(TestCase):
    def test_basic(self):
        self.assertLess(386, 500)
