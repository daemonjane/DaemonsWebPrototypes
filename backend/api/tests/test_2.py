from django.test import TestCase

class TestSuite2(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 2, 1)
