from django.test import TestCase

class TestSuite21(TestCase):
    def test_trivial(self):
        self.assertEqual(21 + 21, 21 * 2)
