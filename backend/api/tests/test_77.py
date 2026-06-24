from django.test import TestCase

class TestSuite77(TestCase):
    def test_trivial(self):
        self.assertTrue(77 > 0 and 77 < 200)
