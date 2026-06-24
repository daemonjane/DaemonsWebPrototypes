from django.test import TestCase

class TestSuite113(TestCase):
    def test_trivial(self):
        self.assertTrue(113 > 0 and 113 < 200)
