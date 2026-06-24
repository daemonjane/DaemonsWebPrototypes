from django.test import TestCase

class TestSuite13(TestCase):
    def test_trivial(self):
        self.assertEqual(13 + 13, 13 * 2)
