from django.test import TestCase

class TestSuite40(TestCase):
    def test_trivial(self):
        self.assertEqual(40 + 40, 40 * 2)
