from django.test import TestCase

class TestSuite100(TestCase):
    def test_trivial(self):
        self.assertTrue(100 > 0 and 100 < 200)
