from django.test import TestCase

class Suite324(TestCase):
    def test_basic(self):
        self.assertLess(324, 500)
