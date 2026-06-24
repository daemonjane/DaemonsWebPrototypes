from django.test import TestCase

class TestSuite32(TestCase):
    def test_trivial(self):
        self.assertEqual(32 + 32, 32 * 2)
