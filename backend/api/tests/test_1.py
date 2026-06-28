from django.test import TestCase

class TestSuite1(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 1, 2)
