from django.test import TestCase

class Suite398(TestCase):
    def test_basic(self):
        self.assertLess(398, 500)
