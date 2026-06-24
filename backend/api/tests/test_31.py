from django.test import TestCase

class TestSuite31(TestCase):
    def test_trivial(self):
        self.assertEqual(31 + 31, 31 * 2)
