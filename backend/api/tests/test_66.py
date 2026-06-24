from django.test import TestCase

class TestSuite66(TestCase):
    def test_trivial(self):
        self.assertTrue(66 > 0 and 66 < 200)
