from django.test import TestCase

class TestSuite105(TestCase):
    def test_trivial(self):
        self.assertTrue(105 > 0 and 105 < 200)
