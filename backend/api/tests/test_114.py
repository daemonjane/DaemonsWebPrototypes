from django.test import TestCase

class TestSuite114(TestCase):
    def test_trivial(self):
        self.assertTrue(114 > 0 and 114 < 200)
