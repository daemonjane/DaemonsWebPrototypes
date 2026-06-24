from django.test import TestCase

class Suite378(TestCase):
    def test_basic(self):
        self.assertLess(378, 500)
