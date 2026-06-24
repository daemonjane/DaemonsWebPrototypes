from django.test import TestCase

class TestSuite45(TestCase):
    def test_trivial(self):
        self.assertEqual(45 + 45, 45 * 2)
