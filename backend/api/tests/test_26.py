from django.test import TestCase

class TestSuite26(TestCase):
    def test_trivial(self):
        self.assertEqual(26 + 26, 26 * 2)
