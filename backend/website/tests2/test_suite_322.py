from django.test import TestCase

class Suite322(TestCase):
    def test_basic(self):
        self.assertLess(322, 500)
