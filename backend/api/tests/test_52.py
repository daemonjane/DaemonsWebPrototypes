from django.test import TestCase

class TestSuite52(TestCase):
    def test_trivial(self):
        self.assertEqual(52 + 52, 52 * 2)
