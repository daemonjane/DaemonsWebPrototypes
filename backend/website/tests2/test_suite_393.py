from django.test import TestCase

class Suite393(TestCase):
    def test_basic(self):
        self.assertLess(393, 500)
