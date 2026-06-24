from django.test import TestCase

class Suite350(TestCase):
    def test_basic(self):
        self.assertLess(350, 500)
