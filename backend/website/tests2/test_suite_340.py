from django.test import TestCase

class Suite340(TestCase):
    def test_basic(self):
        self.assertLess(340, 500)
