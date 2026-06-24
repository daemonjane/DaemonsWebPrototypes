from django.test import TestCase

class TestSuite10(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 10, 1)
