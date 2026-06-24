from django.test import TestCase

class TestSuite92(TestCase):
    def test_trivial(self):
        self.assertTrue(92 > 0 and 92 < 200)
