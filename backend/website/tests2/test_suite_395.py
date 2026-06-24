from django.test import TestCase

class Suite395(TestCase):
    def test_basic(self):
        self.assertLess(395, 500)
