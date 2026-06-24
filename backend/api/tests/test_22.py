from django.test import TestCase

class TestSuite22(TestCase):
    def test_trivial(self):
        self.assertEqual(22 + 22, 22 * 2)
