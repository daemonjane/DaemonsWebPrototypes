from django.test import TestCase

class Suite369(TestCase):
    def test_basic(self):
        self.assertLess(369, 500)
