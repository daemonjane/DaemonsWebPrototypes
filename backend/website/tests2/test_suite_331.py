from django.test import TestCase

class Suite331(TestCase):
    def test_basic(self):
        self.assertLess(331, 500)
