from django.test import TestCase

class TestSuite6(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 6, 1)
