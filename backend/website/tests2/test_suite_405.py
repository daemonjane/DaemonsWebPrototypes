from django.test import TestCase

class Suite405(TestCase):
    def test_basic(self):
        self.assertLess(405, 500)
