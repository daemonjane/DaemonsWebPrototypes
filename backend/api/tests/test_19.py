from django.test import TestCase

class TestSuite19(TestCase):
    def test_trivial(self):
        self.assertEqual(19 + 19, 19 * 2)
