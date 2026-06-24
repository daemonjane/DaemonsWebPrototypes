from django.test import TestCase

class Suite407(TestCase):
    def test_basic(self):
        self.assertLess(407, 500)
