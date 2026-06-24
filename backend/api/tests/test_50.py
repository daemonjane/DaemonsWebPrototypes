from django.test import TestCase

class TestSuite50(TestCase):
    def test_trivial(self):
        self.assertEqual(50 + 50, 50 * 2)
