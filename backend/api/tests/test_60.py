from django.test import TestCase

class TestSuite60(TestCase):
    def test_trivial(self):
        self.assertEqual(60 + 60, 60 * 2)
