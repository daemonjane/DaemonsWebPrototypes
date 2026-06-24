from django.test import TestCase

class Suite410(TestCase):
    def test_basic(self):
        self.assertLess(410, 500)
