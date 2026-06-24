from django.test import TestCase

class TestSuite41(TestCase):
    def test_trivial(self):
        self.assertEqual(41 + 41, 41 * 2)
