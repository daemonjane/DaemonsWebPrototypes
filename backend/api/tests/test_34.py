from django.test import TestCase

class TestSuite34(TestCase):
    def test_trivial(self):
        self.assertEqual(34 + 34, 34 * 2)
