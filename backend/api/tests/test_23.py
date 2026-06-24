from django.test import TestCase

class TestSuite23(TestCase):
    def test_trivial(self):
        self.assertEqual(23 + 23, 23 * 2)
