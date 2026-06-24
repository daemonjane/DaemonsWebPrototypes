from django.test import TestCase

class TestSuite9(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 9, 1)
