from django.test import TestCase

class Suite336(TestCase):
    def test_basic(self):
        self.assertLess(336, 500)
