from django.test import TestCase

class Suite384(TestCase):
    def test_basic(self):
        self.assertLess(384, 500)
