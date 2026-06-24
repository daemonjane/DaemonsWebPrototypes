from django.test import TestCase

class Suite333(TestCase):
    def test_basic(self):
        self.assertLess(333, 500)
