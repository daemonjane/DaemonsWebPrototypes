from django.test import TestCase

class Suite420(TestCase):
    def test_basic(self):
        self.assertLess(420, 500)
