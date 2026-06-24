from django.test import TestCase

class Suite418(TestCase):
    def test_basic(self):
        self.assertLess(418, 500)
