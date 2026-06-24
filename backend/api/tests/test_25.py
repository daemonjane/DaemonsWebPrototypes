from django.test import TestCase

class TestSuite25(TestCase):
    def test_trivial(self):
        self.assertEqual(25 + 25, 25 * 2)
