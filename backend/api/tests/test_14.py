from django.test import TestCase

class TestSuite14(TestCase):
    def test_trivial(self):
        self.assertEqual(14 + 14, 14 * 2)
