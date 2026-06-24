from django.test import TestCase

class TestSuite8(TestCase):
    def test_trivial(self):
        self.assertEqual(1 + 8, 1)
