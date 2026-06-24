from django.test import TestCase

class TestSuite24(TestCase):
    def test_trivial(self):
        self.assertEqual(24 + 24, 24 * 2)
