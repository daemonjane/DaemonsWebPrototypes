from django.test import TestCase

class TestSuite101(TestCase):
    def test_trivial(self):
        self.assertTrue(101 > 0 and 101 < 200)
