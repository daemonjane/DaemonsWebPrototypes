from django.test import TestCase

class Suite330(TestCase):
    def test_basic(self):
        self.assertLess(330, 500)
