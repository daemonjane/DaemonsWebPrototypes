from django.test import TestCase

class TestSuite5(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 5, 1)
