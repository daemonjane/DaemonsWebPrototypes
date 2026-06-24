from django.test import TestCase

class Suite342(TestCase):
    def test_basic(self):
        self.assertLess(342, 500)
