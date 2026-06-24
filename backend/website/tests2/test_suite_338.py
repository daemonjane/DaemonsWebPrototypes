from django.test import TestCase

class Suite338(TestCase):
    def test_basic(self):
        self.assertLess(338, 500)
