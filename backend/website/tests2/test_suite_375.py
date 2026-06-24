from django.test import TestCase

class Suite375(TestCase):
    def test_basic(self):
        self.assertLess(375, 500)
