from django.test import TestCase

class Suite406(TestCase):
    def test_basic(self):
        self.assertLess(406, 500)
