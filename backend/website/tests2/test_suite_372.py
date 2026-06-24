from django.test import TestCase

class Suite372(TestCase):
    def test_basic(self):
        self.assertLess(372, 500)
