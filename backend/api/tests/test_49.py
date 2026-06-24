from django.test import TestCase

class TestSuite49(TestCase):
    def test_trivial(self):
        self.assertEqual(49 + 49, 49 * 2)
