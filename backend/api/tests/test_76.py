from django.test import TestCase

class TestSuite76(TestCase):
    def test_trivial(self):
        self.assertTrue(76 > 0 and 76 < 200)
