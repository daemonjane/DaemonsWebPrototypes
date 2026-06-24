from django.test import TestCase

class TestSuite64(TestCase):
    def test_trivial(self):
        self.assertTrue(64 > 0 and 64 < 200)
