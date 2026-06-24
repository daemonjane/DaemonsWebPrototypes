from django.test import TestCase

class Suite413(TestCase):
    def test_basic(self):
        self.assertLess(413, 500)
