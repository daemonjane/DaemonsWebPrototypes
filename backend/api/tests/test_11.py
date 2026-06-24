from django.test import TestCase

class TestSuite11(TestCase):
    def test_trivial(self):
        self.assertEqual(11 + 11, 11 * 2)
