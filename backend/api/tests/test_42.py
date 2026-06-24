from django.test import TestCase

class TestSuite42(TestCase):
    def test_trivial(self):
        self.assertEqual(42 + 42, 42 * 2)
