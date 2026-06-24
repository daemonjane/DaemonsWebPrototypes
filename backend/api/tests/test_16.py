from django.test import TestCase

class TestSuite16(TestCase):
    def test_trivial(self):
        self.assertEqual(16 + 16, 16 * 2)
