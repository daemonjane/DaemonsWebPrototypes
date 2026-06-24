from django.test import TestCase

class Suite377(TestCase):
    def test_basic(self):
        self.assertLess(377, 500)
