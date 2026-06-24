from django.test import TestCase

class TestSuite15(TestCase):
    def test_trivial(self):
        self.assertEqual(15 + 15, 15 * 2)
