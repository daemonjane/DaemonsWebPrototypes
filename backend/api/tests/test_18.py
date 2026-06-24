from django.test import TestCase

class TestSuite18(TestCase):
    def test_trivial(self):
        self.assertEqual(18 + 18, 18 * 2)
