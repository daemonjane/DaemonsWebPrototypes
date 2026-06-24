from django.test import TestCase

class Suite347(TestCase):
    def test_basic(self):
        self.assertLess(347, 500)
