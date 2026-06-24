from django.test import TestCase

class Suite412(TestCase):
    def test_basic(self):
        self.assertLess(412, 500)
