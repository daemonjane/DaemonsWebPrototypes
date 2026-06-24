from django.test import TestCase

class TestSuite106(TestCase):
    def test_trivial(self):
        self.assertTrue(106 > 0 and 106 < 200)
