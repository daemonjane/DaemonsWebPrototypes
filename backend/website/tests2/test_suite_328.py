from django.test import TestCase

class Suite328(TestCase):
    def test_basic(self):
        self.assertLess(328, 500)
