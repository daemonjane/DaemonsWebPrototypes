from django.test import TestCase

class TestSuite17(TestCase):
    def test_trivial(self):
        self.assertEqual(17 + 17, 17 * 2)
