from django.test import TestCase

class TestSuite51(TestCase):
    def test_trivial(self):
        self.assertEqual(51 + 51, 51 * 2)
