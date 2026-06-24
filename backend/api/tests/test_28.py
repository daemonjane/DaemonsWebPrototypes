from django.test import TestCase

class TestSuite28(TestCase):
    def test_trivial(self):
        self.assertEqual(28 + 28, 28 * 2)
